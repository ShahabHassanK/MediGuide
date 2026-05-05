import json
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from agent.state import MediGuideState
from agent.prompts import SYSTEM_PROMPT
from agent.tools import (
    search_medical_knowledge,
    search_patient_documents,
    find_conditions_for_symptoms,
    get_treatments_for_condition,
)
from config import settings

# In-memory session store — Redis would replace this in production
sessions: dict[str, MediGuideState] = {}

_llm = ChatGroq(api_key=settings.groq_api_key, model="llama-3.3-70b-versatile", temperature=0.3)


def _init_state(session_id: str) -> MediGuideState:
    return MediGuideState(
        messages=[],
        symptoms_mentioned=[],
        patient_context={},
        session_id=session_id,
        current_query="",
        neo4j_context="",
        qdrant_context="",
        uploaded_doc_ids=[],
        final_response="",
        tool_plan={},
    )


async def extract_symptoms_node(state: MediGuideState) -> dict:
    history_text = "\n".join(
        f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
        for m in state["messages"][-6:]
    )
    prompt = f"""Given this conversation and the current message, extract any symptoms or medical conditions mentioned by the user.
Also note if the user mentioned their age, existing conditions, or medications.

Conversation history:
{history_text}

Current message: {state['current_query']}

Respond with JSON only in this exact format:
{{"symptoms": ["symptom1", "symptom2"], "patient_updates": {{"age": null, "conditions": [], "medications": []}}}}

If nothing relevant is found, return empty lists. Only extract what the user mentioned, not the assistant."""

    response = _llm.invoke([HumanMessage(content=prompt)])
    try:
        data = json.loads(response.content)
    except Exception:
        data = {"symptoms": [], "patient_updates": {}}

    new_symptoms = data.get("symptoms", [])
    existing = state["symptoms_mentioned"]
    merged = list({s.lower(): s for s in existing + new_symptoms}.values())

    patient_context = dict(state["patient_context"])
    updates = data.get("patient_updates", {})
    if updates.get("age"):
        patient_context["age"] = updates["age"]
    if updates.get("conditions"):
        patient_context.setdefault("conditions", [])
        patient_context["conditions"] = list(set(patient_context["conditions"] + updates["conditions"]))
    if updates.get("medications"):
        patient_context.setdefault("medications", [])
        patient_context["medications"] = list(set(patient_context["medications"] + updates["medications"]))

    return {"symptoms_mentioned": merged, "patient_context": patient_context}


async def decide_tools_node(state: MediGuideState) -> dict:
    symptoms_str = ", ".join(state["symptoms_mentioned"]) if state["symptoms_mentioned"] else "none"
    patient_str = json.dumps(state["patient_context"]) if state["patient_context"] else "none"

    prompt = f"""You are deciding which data sources to query to answer a medical question.

Current question: {state['current_query']}
Symptoms mentioned so far: {symptoms_str}
Patient context: {patient_str}
User has uploaded documents: {'yes' if state['uploaded_doc_ids'] else 'no'}

Decide which tools are needed. Respond with JSON only:
{{"use_qdrant": true, "use_neo4j": false}}

Rules:
- use_qdrant=true if the question asks about a condition, medication, treatment, or general medical knowledge
- use_neo4j=true if there are symptoms to look up or the question asks about conditions or treatments by name
- use_qdrant=false only for simple greetings or purely conversational messages with no health content
- use_neo4j=false if no symptoms have been mentioned and no condition names appear in the question"""

    response = _llm.invoke([HumanMessage(content=prompt)])
    try:
        plan = json.loads(response.content)
    except Exception:
        plan = {"use_qdrant": True, "use_neo4j": False}

    return {"tool_plan": plan}


async def query_qdrant_node(state: MediGuideState) -> dict:
    from db.qdrant_client import get_qdrant_client
    client = get_qdrant_client()

    knowledge = await search_medical_knowledge(state["current_query"], client)
    doc_results = ""
    if state["uploaded_doc_ids"]:
        doc_results = await search_patient_documents(state["current_query"], state["uploaded_doc_ids"], client)

    combined = knowledge
    if doc_results:
        combined = (combined + "\n\nFrom your uploaded documents:\n" + doc_results) if combined else doc_results

    return {"qdrant_context": combined}


async def query_neo4j_node(state: MediGuideState) -> dict:
    from db.neo4j_client import get_neo4j_driver
    driver = get_neo4j_driver()

    parts = []
    if state["symptoms_mentioned"]:
        conditions_text = await find_conditions_for_symptoms(state["symptoms_mentioned"], driver)
        if conditions_text:
            parts.append(conditions_text)

    query_lower = state["current_query"].lower()
    condition_keywords = [
        "diabetes", "hypertension", "asthma", "arthritis", "depression", "anxiety",
        "cancer", "flu", "pneumonia", "migraine", "obesity", "anemia", "infection",
        "heart disease", "stroke", "alzheimer", "parkinson", "epilepsy", "copd",
    ]
    for keyword in condition_keywords:
        if keyword in query_lower:
            treatments_text = await get_treatments_for_condition(keyword, driver)
            if treatments_text:
                parts.append(treatments_text)
            break

    return {"neo4j_context": "\n\n".join(parts)}


async def generate_response_node(state: MediGuideState) -> dict:
    context_parts = []
    if state.get("qdrant_context"):
        context_parts.append(f"Medical Knowledge:\n{state['qdrant_context']}")
    if state.get("neo4j_context"):
        context_parts.append(f"Condition and Treatment Information:\n{state['neo4j_context']}")

    patient_info = ""
    if state["patient_context"]:
        patient_info = f"Patient context: {json.dumps(state['patient_context'])}"
    if state["symptoms_mentioned"]:
        patient_info += f"\nSymptoms mentioned so far: {', '.join(state['symptoms_mentioned'])}"

    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages.extend(state["messages"])

    user_content = state["current_query"]
    if context_parts:
        user_content += "\n\n[Retrieved Context]\n" + "\n\n".join(context_parts)
    if patient_info:
        user_content += f"\n\n[Session Context]\n{patient_info}"

    messages.append(HumanMessage(content=user_content))

    response = _llm.invoke(messages)
    final_text = response.content

    updated_messages = list(state["messages"]) + [
        HumanMessage(content=state["current_query"]),
        AIMessage(content=final_text),
    ]

    return {
        "final_response": final_text,
        "messages": updated_messages,
        "qdrant_context": "",
        "neo4j_context": "",
    }


def _route_from_decide(state: MediGuideState) -> str:
    plan = state.get("tool_plan", {})
    use_qdrant = plan.get("use_qdrant", True)
    use_neo4j = plan.get("use_neo4j", False)
    if use_qdrant:
        return "qdrant"
    if use_neo4j:
        return "neo4j"
    return "none"


def _route_after_qdrant(state: MediGuideState) -> str:
    plan = state.get("tool_plan", {})
    if plan.get("use_neo4j", False):
        return "neo4j"
    return "generate"


def _build_graph():
    graph = StateGraph(MediGuideState)
    graph.add_node("extract_symptoms", extract_symptoms_node)
    graph.add_node("decide_tools", decide_tools_node)
    graph.add_node("query_qdrant", query_qdrant_node)
    graph.add_node("query_neo4j", query_neo4j_node)
    graph.add_node("generate_response", generate_response_node)

    graph.set_entry_point("extract_symptoms")
    graph.add_edge("extract_symptoms", "decide_tools")

    graph.add_conditional_edges(
        "decide_tools",
        _route_from_decide,
        {
            "qdrant": "query_qdrant",
            "neo4j": "query_neo4j",
            "none": "generate_response",
        },
    )
    graph.add_conditional_edges(
        "query_qdrant",
        _route_after_qdrant,
        {
            "neo4j": "query_neo4j",
            "generate": "generate_response",
        },
    )
    graph.add_edge("query_neo4j", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()


_graph = _build_graph()


async def run_agent(session_id: str, user_message: str, uploaded_doc_ids: list = []) -> str:
    if session_id not in sessions:
        sessions[session_id] = _init_state(session_id)

    state = dict(sessions[session_id])
    state["current_query"] = user_message
    state["uploaded_doc_ids"] = uploaded_doc_ids
    state["tool_plan"] = {}

    result = await _graph.ainvoke(state)
    sessions[session_id] = result
    return result["final_response"]
