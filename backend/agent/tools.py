from qdrant_client import QdrantClient
from qdrant_client.models import Filter, HasIdCondition
from neo4j import Driver

from config import settings
from ingestion.embedder import embed_single


async def search_medical_knowledge(query: str, qdrant_client: QdrantClient, top_k: int = 5) -> str:
    try:
        vector = embed_single(query)
        results = qdrant_client.search(
            collection_name=settings.qdrant_collection_name,
            query_vector=vector,
            limit=top_k,
            with_payload=True,
        )
    except Exception:
        return ""
    if not results:
        return ""
    passages = []
    for i, hit in enumerate(results, 1):
        payload = hit.payload or {}
        source = payload.get("source", "unknown")
        topic = payload.get("topic", "")
        text = payload.get("text", "")
        passages.append(f"{i}. [{source}] {topic}\n{text}")
    return "\n\n".join(passages)


async def search_patient_documents(query: str, doc_ids: list, qdrant_client: QdrantClient, top_k: int = 3) -> str:
    if not doc_ids:
        return ""
    try:
        vector = embed_single(query)
        results = qdrant_client.search(
            collection_name=settings.qdrant_collection_name,
            query_vector=vector,
            query_filter=Filter(must=[HasIdCondition(has_id=doc_ids)]),
            limit=top_k,
            with_payload=True,
        )
    except Exception:
        return ""
    if not results:
        return ""
    passages = []
    for i, hit in enumerate(results, 1):
        payload = hit.payload or {}
        filename = payload.get("title", "uploaded document")
        text = payload.get("text", "")
        passages.append(f"{i}. [Your document: {filename}]\n{text}")
    return "\n\n".join(passages)


async def find_conditions_for_symptoms(symptoms: list, neo4j_driver: Driver) -> str:
    if not symptoms:
        return ""
    cypher = """
    UNWIND $symptoms AS symptomName
    MATCH (s:Symptom)-[:ASSOCIATED_WITH]->(c:Condition)
    WHERE toLower(s.name) CONTAINS toLower(symptomName)
    WITH c, count(DISTINCT s) AS matchCount
    ORDER BY matchCount DESC
    RETURN c.name AS condition, c.description AS description, matchCount
    LIMIT 5
    """
    with neo4j_driver.session(database=settings.neo4j_database) as session:
        results = session.run(cypher, {"symptoms": symptoms})
        rows = [record.data() for record in results]
    if not rows:
        return ""
    lines = ["Conditions related to the mentioned symptoms:"]
    for row in rows:
        match_word = "symptom" if row["matchCount"] == 1 else "symptoms"
        lines.append(
            f"{row['condition']} (matches {row['matchCount']} {match_word}): {row.get('description', '')}"
        )
    return "\n".join(lines)


async def get_treatments_for_condition(condition_name: str, neo4j_driver: Driver) -> str:
    cypher = """
    MATCH (c:Condition)-[:TREATED_BY]->(t:Treatment)
    WHERE toLower(c.name) CONTAINS toLower($condition)
    RETURN c.name AS condition, t.name AS treatment, t.description AS description
    LIMIT 10
    """
    with neo4j_driver.session(database=settings.neo4j_database) as session:
        results = session.run(cypher, {"condition": condition_name})
        rows = [record.data() for record in results]
    if not rows:
        return ""
    lines = [f"Treatments for {condition_name}:"]
    for row in rows:
        lines.append(f"{row['treatment']}: {row.get('description', '')}")
    return "\n".join(lines)
