import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from api.models import UploadResponse
from api.routes.chat import add_doc_ids
from ingestion.chunker import chunk_medlineplus
from ingestion.embedder import embed_texts
from ingestion.vector_store import upload_chunks, ensure_collection
from db.qdrant_client import get_qdrant_client
from config import settings

router = APIRouter()


async def _extract_text(file: UploadFile) -> str:
    filename = file.filename or ""
    content = await file.read()
    if filename.endswith(".pdf"):
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return content.decode("utf-8", errors="ignore")


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    session_id: str = Form(...),
):
    filename = file.filename or "document"
    if not (filename.endswith(".txt") or filename.endswith(".pdf")):
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported.")

    text = await _extract_text(file)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from the file.")

    doc = {
        "text": text,
        "title": filename,
        "url": "",
        "source": "user_upload",
        "topic": filename,
        "session_id": session_id,
    }
    chunks = chunk_medlineplus(doc)

    client = get_qdrant_client()
    ensure_collection(client, settings.qdrant_collection_name)

    texts = [c["text"] for c in chunks]
    vectors = embed_texts(texts)

    point_ids = [str(uuid.uuid4()) for _ in chunks]
    for chunk, pid in zip(chunks, point_ids):
        chunk["_point_id"] = pid

    upload_chunks(chunks, vectors, client, point_ids=point_ids)
    add_doc_ids(session_id, point_ids)

    return UploadResponse(
        session_id=session_id,
        doc_id=point_ids[0] if point_ids else "",
        filename=filename,
        chunks_stored=len(chunks),
    )
