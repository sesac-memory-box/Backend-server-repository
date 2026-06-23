from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from api.schemas import (
    ChatRequest,
    ChatResponse,
    SessionSummaryRequest,
    SessionSummaryResponse,
    STTResponse,
    TTSRequest,
)
from api.services.chat import generate_chat_response
from api.services.rag import initialize_knowledge_base
from api.services.stt import transcribe_audio
from api.services.summary import generate_session_summary
from api.services.tts import synthesize_speech


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_knowledge_base()
    yield


app = FastAPI(
    title="Memory Box RAG Chatbot API",
    description="치매 어르신 회상 대화 API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat/", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return generate_chat_response(request)


@app.post("/chat/summary", response_model=SessionSummaryResponse)
def chat_summary(request: SessionSummaryRequest) -> SessionSummaryResponse:
    return generate_session_summary(request.messages)


@app.post("/stt/", response_model=STTResponse)
async def stt(audio: UploadFile = File(...)) -> STTResponse:
    transcript = await transcribe_audio(audio)
    return STTResponse(transcript=transcript)


@app.post("/tts/")
def tts(request: TTSRequest) -> Response:
    audio_bytes = synthesize_speech(request.text, request.voice)
    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'inline; filename="speech.mp3"'},
    )
