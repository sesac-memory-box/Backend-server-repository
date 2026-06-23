import json

from api.config import OPENAI_API_KEY, SUMMARY_MODEL
from api.schemas import Message, SessionSummaryResponse
from api.services.rag import get_client

SUMMARY_SYSTEM_PROMPT = """당신은 회상 대화 분석 전문가입니다.
대화에서 장소, 인물, 다음 대화 주제를 추출합니다.

반드시 아래 JSON 형식으로만 응답하세요:
{
  "places": ["장소1", "장소2"],
  "people": ["인물1", "인물2"],
  "next_topics": ["주제1", "주제2", "주제3"]
}

규칙:
- places: 대화에서 언급된 장소 이름 목록 (없으면 빈 배열)
- people: 대화에서 언급된 인물 이름 목록 (없으면 빈 배열)
- next_topics: 다음 대화에서 꺼낼 수 있는 주제 정확히 3개
- 한국어로 작성
- JSON 외 다른 텍스트는 출력하지 않음"""


def _format_messages(messages: list[Message]) -> str:
    lines = []
    for message in messages:
        speaker = "사용자" if message.role == "user" else "AI"
        lines.append(f"{speaker}: {message.content}")
    return "\n".join(lines)


def generate_session_summary(messages: list[Message]) -> SessionSummaryResponse:
    if not messages:
        return SessionSummaryResponse(places=[], people=[], next_topics=["", "", ""])

    if not OPENAI_API_KEY:
        return SessionSummaryResponse(
            places=[],
            people=[],
            next_topics=["추억 이야기", "가족 이야기", "좋아하던 음식"],
        )

    conversation = _format_messages(messages)
    response = get_client().chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": f"다음 대화를 분석해 주세요:\n\n{conversation}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()
    data = json.loads(content)

    places = data.get("places") or []
    people = data.get("people") or []
    next_topics = data.get("next_topics") or []

    while len(next_topics) < 3:
        next_topics.append("추억 이야기")
    next_topics = next_topics[:3]

    return SessionSummaryResponse(
        places=places,
        people=people,
        next_topics=next_topics,
    )
