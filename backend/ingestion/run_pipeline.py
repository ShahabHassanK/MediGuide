# Run with: python -m ingestion.run_pipeline  (from backend/)
import json
import os
import sys
import time

from qdrant_client import QdrantClient
from tqdm import tqdm

from config import settings
from db.qdrant_client import get_qdrant_client
from ingestion.chunker import chunk_medlineplus, chunk_medquad
from ingestion.embedder import embed_texts
from ingestion.fetch_medlineplus import fetch_medlineplus_docs
from ingestion.fetch_medquad import fetch_medquad_docs
from ingestion.graph_loader import load_graph
from ingestion.vector_store import ensure_collection, upload_chunks


def _fresh_qdrant() -> QdrantClient:
    """Always returns a brand-new client with a live TCP connection."""
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key, timeout=120)


def _upload_with_retry(batch: list, vectors: list, retries: int = 3):
    """Upload one batch, creating a fresh client on each attempt."""
    for attempt in range(retries):
        try:
            upload_chunks(batch, vectors, _fresh_qdrant())
            return
        except Exception as exc:
            if attempt == retries - 1:
                raise
            wait = 10 * (attempt + 1)
            tqdm.write(f"\n  Upload error (attempt {attempt + 1}/{retries}): {exc}. Retrying in {wait}s...")
            time.sleep(wait)

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), ".pipeline_progress.json")


def _load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {}


def _save_progress(state: dict):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(state, f, indent=2)


def _ingest_medlineplus(qdrant, progress: dict) -> dict:
    if progress.get("medlineplus_done"):
        print("\n=== MedlinePlus Ingestion === [skipped — already done]")
        return progress

    print("\n=== MedlinePlus Ingestion ===")
    docs = fetch_medlineplus_docs(max_docs=45)
    print(f"Fetched {len(docs)} MedlinePlus documents")

    chunks = [chunk for doc in docs for chunk in chunk_medlineplus(doc)]
    print(f"Created {len(chunks)} chunks")

    vectors = embed_texts([c["text"] for c in chunks])
    upload_chunks(chunks, vectors, qdrant)
    print(f"Uploaded {len(chunks)} chunks to Qdrant")

    progress["medlineplus_done"] = True
    _save_progress(progress)
    return progress


def _ingest_medquad(qdrant, progress: dict) -> dict:
    if progress.get("medquad_done"):
        print("\n=== MedQuAD Ingestion === [skipped — already done]")
        return progress

    print("\n=== MedQuAD Ingestion ===")
    docs = fetch_medquad_docs(max_docs=10000)
    print(f"Loaded {len(docs)} MedQuAD documents")

    chunks = [chunk for doc in docs for chunk in chunk_medquad(doc)]
    print(f"Created {len(chunks)} chunks")

    batch_size = 100
    starts = list(range(0, len(chunks), batch_size))
    total_batches = len(starts)
    done = progress.get("medquad_batches_done", 0)

    if done > 0:
        print(f"  Resuming from batch {done}/{total_batches} ({done * batch_size} chunks already uploaded)")

    for i in tqdm(range(done, total_batches), desc="Embedding & uploading", initial=done, total=total_batches):
        batch = chunks[starts[i] : starts[i] + batch_size]
        vectors = embed_texts([c["text"] for c in batch])
        _upload_with_retry(batch, vectors)
        progress["medquad_batches_done"] = i + 1
        _save_progress(progress)

    progress["medquad_done"] = True
    _save_progress(progress)
    print(f"Uploaded {len(chunks)} MedQuAD chunks to Qdrant")
    return progress


def main():
    start = time.time()
    print("Starting MediGuide ingestion pipeline...")

    progress = _load_progress()
    if progress:
        print(f"  Resuming from saved progress: {progress}")

    qdrant = get_qdrant_client()
    ensure_collection(qdrant, settings.qdrant_collection_name)
    print(f"Qdrant collection '{settings.qdrant_collection_name}' ready")

    if "--skip-medlineplus" in sys.argv:
        progress["medlineplus_done"] = True
        _save_progress(progress)
        print("\n=== MedlinePlus Ingestion === [skipped via --skip-medlineplus]")
    else:
        progress = _ingest_medlineplus(qdrant, progress)

    progress = _ingest_medquad(qdrant, progress)

    if not progress.get("graph_done"):
        print("\n=== Neo4j Graph Ingestion ===")
        load_graph()
        progress["graph_done"] = True
        _save_progress(progress)
    else:
        print("\n=== Neo4j Graph Ingestion === [skipped — already done]")

    elapsed = time.time() - start
    print(f"\nIngestion pipeline complete in {elapsed:.1f}s")

    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("Progress checkpoint cleaned up.")


if __name__ == "__main__":
    main()
