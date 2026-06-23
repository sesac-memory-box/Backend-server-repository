from api.config import DEFAULT_TTS_VOICE, OPENAI_API_KEY, TTS_MODEL, VALID_TTS_VOICES
from api.services.rag import get_client


def synthesize_speech(text: str, voice: str = DEFAULT_TTS_VOICE) -> bytes:
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text is required.")

    if voice not in VALID_TTS_VOICES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid voice. Choose one of: {', '.join(sorted(VALID_TTS_VOICES))}",
        )

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key is not configured.")

    try:
        response = get_client().audio.speech.create(
            model=TTS_MODEL,
            voice=voice,
            input=text,
            response_format="mp3",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TTS processing failed: {exc}") from exc

    return response.content
