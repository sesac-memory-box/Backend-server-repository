import io

from fastapi import HTTPException, UploadFile

from api.config import OPENAI_API_KEY, STT_MODEL
from api.services.rag import get_client


async def transcribe_audio(audio: UploadFile) -> str:
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key is not configured.")

    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Audio file is empty.")

    filename = audio.filename or "audio.wav"
    file_obj = io.BytesIO(audio_bytes)
    file_obj.name = filename

    try:
        response = get_client().audio.transcriptions.create(
            model=STT_MODEL,
            file=file_obj,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"STT processing failed: {exc}") from exc

    return response.text.strip()
