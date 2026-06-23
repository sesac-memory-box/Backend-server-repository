from typing import Optional

from api.config import CHAT_MESSAGE_THRESHOLD, CHAT_MODEL, OPENAI_API_KEY, SUMMARY_MODEL
from api.schemas import ChatRequest, ChatResponse, Message
from api.services.rag import get_client, retrieve_context

SYSTEM_PROMPT = """당신은 치매 어르신을 위한 따뜻한 회상 대화 상담사입니다.

역할:
- 어르신의 과거 경험과 추억을 편안하게 떠올리도록 돕습니다.
- 짧고 따뜻한 문장으로 대화합니다.
- 감정을 먼저 공감하고, 감각·경험 중심 질문을 합니다.
- 기억이 틀려도 바로잡지 않습니다.
- 제공된 참고 자료와 대상자 정보를 활용해 자연스럽게 대화를 이어갑니다.

응답 규칙:
- 2~4문장 정도로 간결하게 답합니다.
- 존댓말을 사용합니다.
- 어르신이 대답하기 쉬운 열린 질문으로 마무리합니다."""


def _dedupe_messages(messages: Optional[list[Message]], query: str) -> list[Message]:
    """프론트엔드가 query와 중복된 마지막 user 메시지를 보낼 수 있어 제거합니다."""
    if not messages:
        return []

    cleaned = list(messages)
    if (
        cleaned
        and cleaned[-1].role == "user"
        and cleaned[-1].content.strip() == query.strip()
    ):
        cleaned = cleaned[:-1]

    return cleaned


def _build_chat_messages(
    request: ChatRequest,
    history: list[Message],
    rag_context: str,
) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    if rag_context:
        messages.append(
            {
                "role": "system",
                "content": f"다음은 대화에 활용할 참고 정보입니다:\n\n{rag_context}",
            }
        )

    if request.summary:
        messages.append(
            {
                "role": "system",
                "content": f"이전 대화 요약:\n{request.summary}",
            }
        )

    for message in history:
        messages.append({"role": message.role, "content": message.content})

    messages.append({"role": "user", "content": request.query})
    return messages


def _generate_answer(chat_messages: list[dict[str, str]]) -> str:
    if not OPENAI_API_KEY:
        return "죄송합니다. AI 서비스 설정이 완료되지 않았습니다."

    response = get_client().chat.completions.create(
        model=CHAT_MODEL,
        messages=chat_messages,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def _compress_conversation(
    previous_summary: Optional[str],
    history: list[Message],
    latest_user: str,
    latest_assistant: str,
) -> str:
    conversation_lines = []
    for message in history:
        speaker = "사용자" if message.role == "user" else "AI"
        conversation_lines.append(f"{speaker}: {message.content}")

    conversation_lines.append(f"사용자: {latest_user}")
    conversation_lines.append(f"AI: {latest_assistant}")
    conversation_text = "\n".join(conversation_lines)

    prompt = f"""다음 대화 내용을 압축 요약해 주세요.

요구사항:
- 핵심 주제, 언급된 사람·장소, 감정 흐름을 포함합니다.
- 5~8문장으로 작성합니다.
- 이후 대화를 이어가기 위한 맥락이 남도록 합니다.

이전 요약:
{previous_summary or "없음"}

새로운 대화:
{conversation_text}
"""

    response = get_client().chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "당신은 대화 요약 전문가입니다. 한국어로 간결하게 요약합니다.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def generate_chat_response(request: ChatRequest) -> ChatResponse:
    history = _dedupe_messages(request.messages, request.query)
    rag_context = retrieve_context(request.query, request.user_id)
    chat_messages = _build_chat_messages(request, history, rag_context)
    answer = _generate_answer(chat_messages)

    new_summary = None
    total_messages = len(history) + 2  # current user + assistant turn

    if total_messages >= CHAT_MESSAGE_THRESHOLD and OPENAI_API_KEY:
        new_summary = _compress_conversation(
            request.summary,
            history,
            request.query,
            answer,
        )

    return ChatResponse(answer=answer, summary=new_summary)
