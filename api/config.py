import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_PATH = BASE_DIR / "data" / "knowledge.txt"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
TTS_MODEL = os.getenv("TTS_MODEL", "tts-1")
STT_MODEL = os.getenv("STT_MODEL", "whisper-1")

CHAT_MESSAGE_THRESHOLD = int(os.getenv("CHAT_MESSAGE_THRESHOLD", "10"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))

VALID_TTS_VOICES = {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}
DEFAULT_TTS_VOICE = "alloy"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "memory_box"),
    "charset": "utf8mb4",
}
