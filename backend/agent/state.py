from typing import TypedDict


class MediGuideState(TypedDict):
    messages: list
    symptoms_mentioned: list
    patient_context: dict
    session_id: str
    current_query: str
    neo4j_context: str
    qdrant_context: str
    uploaded_doc_ids: list
    final_response: str
    tool_plan: dict  # routing decision from decide_tools_node
