import math
import re
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

from api.config import EMBEDDING_MODEL, KNOWLEDGE_PATH, OPENAI_API_KEY, RAG_TOP_K
from api.database import format_user_context, get_user_profile

_client: Optional[OpenAI] = None
_knowledge_chunks: list[str] = []
_knowledge_embeddings: list[list[float]] = []


@dataclass
class KnowledgeChunk:
    topic: str
    content: str

    @property
    def text(self) -> str:
        return f"[{self.topic}] {self.content}"


def _is_valid_api_key() -> bool:
    key = OPENAI_API_KEY.strip()
    return bool(key) and "your_openai_api_key" not in key


def get_client() -> OpenAI:
    global _client
    if _client is None:
        if not _is_valid_api_key():
            raise ValueError("OpenAI API key is not configured.")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _parse_knowledge_file() -> list[KnowledgeChunk]:
    if not KNOWLEDGE_PATH.exists():
        return []

    raw = KNOWLEDGE_PATH.read_text(encoding="utf-8")
    blocks = [block.strip() for block in raw.split("---") if block.strip()]
    chunks: list[KnowledgeChunk] = []

    for block in blocks:
        topic_match = re.search(r"topic:\s*(.+)", block)
        content_match = re.search(r"content:\s*(.+)", block, re.DOTALL)
        if topic_match and content_match:
            chunks.append(
                KnowledgeChunk(
                    topic=topic_match.group(1).strip(),
                    content=content_match.group(1).strip(),
                )
            )

    return chunks


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts or not _is_valid_api_key():
        return []

    response = get_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]


def initialize_knowledge_base() -> None:
    """지식 베이스를 로드하고 임베딩을 생성합니다."""
    global _knowledge_chunks, _knowledge_embeddings

    chunks = _parse_knowledge_file()
    _knowledge_chunks = [chunk.text for chunk in chunks]
    _knowledge_embeddings = []

    if not _knowledge_chunks or not _is_valid_api_key():
        return

    try:
        _knowledge_embeddings = _embed_texts(_knowledge_chunks)
    except Exception as exc:
        print(f"[WARN] Knowledge base embedding failed: {exc}")
        _knowledge_embeddings = []


def retrieve_context(query: str, user_id: Optional[int] = None, top_k: int = RAG_TOP_K) -> str:
    """RAG 검색으로 관련 컨텍스트를 반환합니다."""
    context_parts: list[str] = []

    if user_id:
        user = get_user_profile(user_id)
        if user:
            context_parts.append("=== 대상자 정보 ===")
            context_parts.append(format_user_context(user))

    if _knowledge_chunks and _knowledge_embeddings and _is_valid_api_key():
        try:
            query_embedding = _embed_texts([query])[0]
            if query_embedding:
                scored = [
                    (_cosine_similarity(query_embedding, embedding), chunk)
                    for chunk, embedding in zip(_knowledge_chunks, _knowledge_embeddings)
                ]
                scored.sort(key=lambda item: item[0], reverse=True)
                selected = [chunk for score, chunk in scored[:top_k] if score > 0]

                if selected:
                    context_parts.append("=== 회상 대화 참고 자료 ===")
                    context_parts.extend(selected)
        except Exception as exc:
            print(f"[WARN] RAG retrieval failed: {exc}")

    return "\n\n".join(context_parts)
