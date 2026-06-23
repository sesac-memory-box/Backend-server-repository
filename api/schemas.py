from typing import Literal, Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    query: str
    messages: Optional[list[Message]] = None
    summary: Optional[str] = None
    user_id: Optional[int] = None


class ChatResponse(BaseModel):
    answer: str
    summary: Optional[str] = None


class SessionSummaryRequest(BaseModel):
    messages: list[Message]


class SessionSummaryResponse(BaseModel):
    places: list[str]
    people: list[str]
    next_topics: list[str]


class STTResponse(BaseModel):
    transcript: str


class TTSRequest(BaseModel):
    text: str
    voice: str = "alloy"
