from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str


class TranscribeResponse(BaseModel):
    session_id: str
    transcript: str


class UploadResponse(BaseModel):
    session_id: str
    doc_id: str
    filename: str
    chunks_stored: int
