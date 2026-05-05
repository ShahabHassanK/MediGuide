import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType,
)
from config import settings


def ensure_collection(client: QdrantClient, collection_name: str):
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    for field in ("source", "topic", "session_id"):
        try:
            client.create_payload_index(
                collection_name=collection_name,
                field_name=field,
                field_schema=PayloadSchemaType.KEYWORD,
            )
        except Exception:
            pass


def upload_chunks(chunks: list[dict], vectors: list[list[float]], client: QdrantClient, point_ids: list[str] | None = None):
    if point_ids is None:
        point_ids = [str(uuid.uuid4()) for _ in chunks]

    points = []
    for chunk, vector, pid in zip(chunks, vectors, point_ids):
        payload = {k: v for k, v in chunk.items() if not k.startswith("_")}
        payload.setdefault("session_id", "")
        points.append(PointStruct(id=pid, vector=vector, payload=payload))

    batch_size = 100
    for i in range(0, len(points), batch_size):
        client.upsert(
            collection_name=settings.qdrant_collection_name,
            points=points[i:i + batch_size],
        )
