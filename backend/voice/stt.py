import os
import tempfile
from faster_whisper import WhisperModel

_model = WhisperModel("tiny", device="cpu", compute_type="int8")


async def transcribe_audio(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        segments, _ = _model.transcribe(tmp_path, beam_size=5)
        return " ".join(segment.text.strip() for segment in segments)
    finally:
        os.unlink(tmp_path)
