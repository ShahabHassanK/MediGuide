from fastapi import APIRouter
from api.models import ChatRequest, ChatResponse
from agent.graph import run_agent

router = APIRouter()

# Per-session uploaded doc IDs — keyed by session_id
_session_doc_ids: dict[str, list] = {}


def get_session_doc_ids(session_id: str) -> list:
    return _session_doc_ids.get(session_id, [])


def add_doc_ids(session_id: str, doc_ids: list):
    _session_doc_ids.setdefault(session_id, [])
    _session_doc_ids[session_id].extend(doc_ids)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    doc_ids = get_session_doc_ids(request.session_id)
    response_text = await run_agent(request.session_id, request.message, doc_ids)
    return ChatResponse(session_id=request.session_id, response=response_text)
