import base64
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response
from pydantic import BaseModel

from api.models import TranscribeResponse
from voice.stt import transcribe_audio
from voice.tts import synthesize_speech
from agent.graph import run_agent
from api.routes.chat import get_session_doc_ids

router = APIRouter()


class SynthesizeRequest(BaseModel):
    session_id: str
    text: str


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(
    audio: UploadFile = File(...),
    session_id: str = Form(...),
):
    audio_bytes = await audio.read()
    transcript = await transcribe_audio(audio_bytes)
    return TranscribeResponse(session_id=session_id, transcript=transcript)


@router.post("/synthesize")
async def synthesize(request: SynthesizeRequest):
    audio_bytes = await synthesize_speech(request.text)
    return Response(content=audio_bytes, media_type="audio/mpeg")


@router.post("/conversation")
async def voice_conversation(
    audio: UploadFile = File(...),
    session_id: str = Form(...),
):
    audio_bytes = await audio.read()
    transcript = await transcribe_audio(audio_bytes)
    doc_ids = get_session_doc_ids(session_id)
    response_text = await run_agent(session_id, transcript, doc_ids)
    audio_response = await synthesize_speech(response_text)
    audio_b64 = base64.b64encode(audio_response).decode("utf-8")
    return {
        "session_id": session_id,
        "transcript": transcript,
        "response": response_text,
        "audio_b64": audio_b64,
    }
