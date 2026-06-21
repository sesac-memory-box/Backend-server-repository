"""
AI 대화 페이지
AI와 회상 대화하기
"""

import streamlit as st
from datetime import datetime
from typing import Optional
import os
import sys
import requests
import sounddevice as sd
from scipy.io import wavfile
import numpy as np
import io

# 프로젝트 루트를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_user import UserManager
from database.db_chat import ChatManager
from database.db_history import HistoryManager

# FastAPI 백엔드 URL 설정
API_URL = "http://127.0.0.1:8000"


# 페이지 설정
st.set_page_config(
    page_title="AI 대화 - 기억상자 AI",
    page_icon="💬",
    layout="wide"
)

# 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background-color: #FFF8DC;
    }

    [data-testid="stSidebarNav"] ul li:first-child a {
        font-size: 0;
    }

    [data-testid="stSidebarNav"] ul li:first-child a span {
        display: none;
    }

    [data-testid="stSidebarNav"] ul li:first-child a::after {
        content: "메인 페이지";
        display: inline-block;
        font-size: 1rem;
        color: #333;
    }

    /* 셀렉트박스 드롭다운 옵션 강제 흰색 */
    div[data-baseweb="select"] > div > div > div > div > div,
    div[data-baseweb="select"] > div > div > div > div > div > div,
    div[data-baseweb="select"] > div > div > div > div > div > div > div,
    div[data-baseweb="select"] > div > div > div > div > div > div > div > div,
    div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div {
        background-color: white !important;
        color: #333 !important;
    }

    /* 드롭다운 메뉴 아이템 */
    div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div,
    div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div {
        background-color: white !important;
        color: #333 !important;
    }

    /* 드롭다운 메뉴 아이템 hover */
    div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div:hover,
    div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div:hover {
        background-color: #E8DCC4 !important;
        color: #333 !important;
    }

    /* option 태그 강제 흰색 */
    option {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* 채팅 컨테이너 */
    .chat-container {
        background-color: #FAFAF0;
        padding: 2rem;
        border-radius: 20px;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        margin: 1rem 0;
        box-shadow: inset 0 2px 10px rgba(139, 69, 19, 0.05);
    }
    
    /* 사용자 메시지 */
    .message-user {
        background-color: #E8DCC4;
        padding: 1.2rem;
        border-radius: 18px;
        margin: 1rem 0;
        margin-left: 15%;
        text-align: left;
        box-shadow: 0 2px 8px rgba(139, 69, 19, 0.1);
    }
    
    /* AI 메시지 */
    .message-ai {
        background-color: #D2691E;
        color: white;
        padding: 1.2rem;
        border-radius: 18px;
        margin: 1rem 0;
        margin-right: 15%;
        box-shadow: 0 2px 8px rgba(139, 69, 19, 0.2);
    }
    
    /* 메시지 라벨 */
    .message-label {
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    /* 입력 컨테이너 */
    .input-container {
        background-color: #FFF;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1rem;
        box-shadow: 0 2px 10px rgba(139, 69, 19, 0.1);
    }
    
    /* 대화 정보 */
    .conversation-info {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5F5DC 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #D2691E;
    }
    
    /* 제안 칩 */
    .suggestion-chip {
        display: inline-block;
        background-color: #F5F5DC;
        padding: 0.7rem 1.2rem;
        border-radius: 20px;
        margin: 0.4rem;
        cursor: pointer;
        border: 2px solid #D2691E;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    
    .suggestion-chip:hover {
        background-color: #E8DCC4;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(139, 69, 19, 0.15);
    }
    
    /* 버튼 */
    .stButton>button {
        background-color: #D2B48C;
        color: #333 !important;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #C4A574;
        color: #333 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
    }
    
    /* 텍스트 색상 */
    .stMarkdown, p, span, div, label {
        color: #333 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #8B4513 !important;
    }
    
    input, textarea, select {
        color: #333 !important;
        background-color: white !important;
    }

    /* Streamlit selectbox: selected value and dropdown menu */
    .stSelectbox label {
        color: #333 !important;
        font-weight: 600 !important;
    }

    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div {
        background-color: white !important;
        color: #111 !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        border: 2px solid #E8DCC4 !important;
        border-radius: 12px !important;
    }

    .stSelectbox [data-baseweb="select"] input,
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] svg {
        color: #111 !important;
        fill: #111 !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [role="listbox"] {
        background-color: white !important;
        color: #111 !important;
    }

    [data-baseweb="menu"] *,
    [role="listbox"] *,
    [role="option"] {
        background-color: white !important;
        color: #111 !important;
    }

    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background-color: #F5F5DC !important;
        color: #111 !important;
    }
    
    /* 입력 필드 */
    .stTextInput>div>div>input {
        border: 2px solid #E8DCC4;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
        background-color: white !important;
        color: #333 !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #D2691E;
        box-shadow: 0 0 0 3px rgba(210, 105, 30, 0.1);
    }
    
    /* 셀렉트박스 */
    .stSelectbox>div>div>select {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #E8DCC4;
        border-radius: 12px;
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    .stSelectbox>div>div>div {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* 드롭다운 옵션 */
    .stSelectbox [role="listbox"] {
        background-color: white !important;
    }
    
    .stSelectbox [role="option"] {
        color: #333 !important;
        background-color: white !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: #F5F5DC !important;
    }
    
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background-color: #F5F5DC;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """세션 상태 초기화"""
    if 'chat_user_id' not in st.session_state:
        st.session_state.chat_user_id = None
    
    if 'chat_conversation_id' not in st.session_state:
        st.session_state.chat_conversation_id = None
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    if 'chat_api_messages' not in st.session_state:
        st.session_state.chat_api_messages = []

    if 'chat_summary' not in st.session_state:
        st.session_state.chat_summary = None

    if 'waiting_for_ai' not in st.session_state:
        st.session_state.waiting_for_ai = False

    if 'last_ai_audio' not in st.session_state:
        st.session_state.last_ai_audio = None

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""


def generate_ai_response(user_message: str, user_id: Optional[int], summary: Optional[str], api_messages: list) -> dict:
    """FastAPI 백엔드를 호출하여 AI 응답 및 대화 요약본을 가져옵니다."""
    try:
        formatted_messages = []
        for msg in api_messages:
            role = "user" if msg['speaker'] == 'user' else "assistant"
            formatted_messages.append({"role": role, "content": msg['content']})

        payload = {
            "query": user_message,
            "messages": formatted_messages,
            "summary": summary,
            "user_id": user_id
        }

        response = requests.post(f"{API_URL}/chat/", json=payload, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API 오류: {response.text}")
            return {"answer": "죄송합니다. 서버가 응답하지 않습니다.", "summary": None}
    except Exception as e:
        st.error(f"서버 연결 실패: {str(e)}")
        return {"answer": f"API 서버 연결 실패: {str(e)}", "summary": None}


def text_to_speech(text: str) -> Optional[bytes]:
    """텍스트를 음성으로 변환하는 API 호출"""
    try:
        response = requests.post(f"{API_URL}/tts/", json={"text": text, "voice": "alloy"}, timeout=30)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"TTS 호출 오류: {e}")
    return None


def record_microphone(duration: int = 10, sample_rate: int = 16000) -> Optional[bytes]:
    """마이크에서 음성을 녹음하고 WAV 바이트로 반환합니다."""
    try:
        st.info(f"🎤 {duration}초간 녹음 중입니다. 말씀해주세요...")
        
        # 마이크 녹음
        audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype=np.int16)
        sd.wait()
        
        # WAV 파일로 변환
        wav_buffer = io.BytesIO()
        wavfile.write(wav_buffer, sample_rate, audio_data)
        wav_buffer.seek(0)
        
        st.success("✅ 녹음 완료!")
        return wav_buffer.getvalue()
    except Exception as e:
        st.error(f"마이크 녹음 오류: {e}")
    return None


def transcribe_audio_bytes(audio_bytes: bytes) -> Optional[str]:
    """마이크 녹음 바이트 데이터를 STT API로 전송하고 텍스트를 반환합니다."""
    try:
        files = {
            "audio": (
                "recording.wav",
                audio_bytes,
                "audio/wav"
            )
        }
        response = requests.post(f"{API_URL}/stt/", files=files, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get("transcript")
        else:
            st.error(f"STT API 오류: {response.text}")
    except Exception as e:
        st.error(f"STT 호출 오류: {e}")
    return None


def create_session_summary(conversation_id: int, messages: list) -> dict:
    """대화 전체 메시지를 /chat/summary API에 보내고 요약 결과를 반환합니다."""
    try:
        payload = {
            "messages": [
                {"role": msg["role"], "content": msg["content"]}
                for msg in messages
            ]
        }
        response = requests.post(f"{API_URL}/chat/summary", json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"대화 요약 API 오류: {response.text}")
    except Exception as e:
        st.error(f"대화 요약 호출 오류: {e}")
    return {}


def show_user_selector():
    """대상자 선택"""
    st.markdown("### 👤 대화할 어르신을 선택해주세요")
    
    users = UserManager.get_all_users()
    
    if not users:
        st.warning("등록된 대상자가 없습니다.")
        if st.button("➕ 대상자 등록하러 가기"):
            st.switch_page("pages/1_대상정보.py")
        return False
    
    # 대상자 선택
    user_options = {f"{user['name']} ({user['birth_year']}년생)" if user['birth_year'] 
                   else user['name']: user['id'] for user in users}
    
    _, selector_col, _ = st.columns([1, 1.2, 1])
    with selector_col:
        selected_name = st.selectbox(
            "대상자 선택",
            options=list(user_options.keys()),
            key="user_selector"
        )

        start_chat = st.button("대화 시작하기", type="primary", use_container_width=True)
    
    if start_chat:
        user_id = user_options[selected_name]
        st.session_state.chat_user_id = user_id
        
        # 새 대화 세션 생성
        result = ChatManager.create_conversation(user_id)
        if result:
            conversation_id, session_id = result
            st.session_state.chat_conversation_id = conversation_id
            st.session_state.chat_messages = []
            st.session_state.chat_api_messages = []
            st.session_state.chat_summary = None
            st.session_state.last_ai_audio = None
            st.session_state.user_input = ""
            
            # 환영 메시지 추가
            user = UserManager.get_user_by_id(user_id)
            welcome_msg = f"안녕하세요, {user['name']}님! 😊 오늘은 어떤 추억을 이야기해볼까요?"
            
            ChatManager.add_message(conversation_id, 'ai', welcome_msg)
            st.session_state.chat_messages.append({
                'speaker': 'ai',
                'content': welcome_msg,
                'timestamp': datetime.now()
            })
            st.session_state.chat_api_messages.append({
                'speaker': 'assistant',
                'content': welcome_msg
            })
            
            st.rerun()
        else:
            st.error("대화 세션 생성에 실패했습니다.")
    
    return False


def show_chat_interface():
    """채팅 인터페이스"""
    # 메시지 전송 후 입력창 초기화를 위한 플래그 확인 (위젯 생성 전)
    if st.session_state.get("clear_input_after_send"):
        st.session_state.user_input = ""
        st.session_state.clear_input_after_send = False
    
    user = UserManager.get_user_by_id(st.session_state.chat_user_id)
    conversation = ChatManager.get_conversation_by_id(st.session_state.chat_conversation_id)
    
    if not user or not conversation:
        st.error("대화 정보를 불러올 수 없습니다.")
        if st.button("처음으로"):
            st.session_state.chat_user_id = None
            st.session_state.chat_conversation_id = None
            st.rerun()
        return
    
    # 헤더
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.markdown(f"### 💬 {user['name']}님과의 대화")
    
    with col2:
        duration = ChatManager.get_conversation_duration(st.session_state.chat_conversation_id)
        if duration:
            minutes = duration // 60
            seconds = duration % 60
            st.caption(f"⏱️ 대화 시간: {minutes}분 {seconds}초 | 💬 메시지: {conversation['message_count']}개")
    
    with col3:
        if st.button("🏠 홈", use_container_width=True):
            st.switch_page("app.py")
    
    # 대화 메시지 로드 (세션에 없으면)
    if not st.session_state.chat_messages:
        messages = ChatManager.get_messages(st.session_state.chat_conversation_id)
        st.session_state.chat_messages = [
            {
                'speaker': msg['speaker'],
                'content': msg['content'],
                'timestamp': msg['timestamp']
            }
            for msg in messages
        ]

        # 초기 API 메시지 목록 구성
        if st.session_state.chat_summary is None:
            st.session_state.chat_api_messages = [
                {
                    'speaker': msg['speaker'],
                    'content': msg['content']
                }
                for msg in messages
            ]
        else:
            st.session_state.chat_api_messages = []

    if st.session_state.chat_summary:
        st.info(f"📝 이전 대화 요약: {st.session_state.chat_summary}")
    
    # 채팅 컨테이너
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_messages:
        if msg['speaker'] == 'user':
            st.markdown(f"""
                <div class="message-user">
                    <div class="message-label">👤 {user['name']}</div>
                    <div>{msg['content']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="message-ai">
                    <div class="message-label">🤖 AI 상담사</div>
                    <div>{msg['content']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.last_ai_audio:
        st.audio(st.session_state.last_ai_audio, format='audio/mp3')
    
    # AI가 응답 중일 때
    if st.session_state.waiting_for_ai:
        st.info("🤔 AI가 생각하고 있습니다...")
    
    # 마이크 녹음 섹션
    st.markdown("---")
    st.markdown("#### 🎤 음성으로 말씀하기")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🎤 녹음 시작", use_container_width=True, key="mic_record_btn"):
            audio_bytes = record_microphone(duration=10)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/wav')
                
                # STT 처리
                transcript = transcribe_audio_bytes(audio_bytes)
                if transcript:
                    st.info(f"📝 인식 결과: {transcript}")
                    st.session_state.user_input = transcript
                    st.rerun()

    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        def on_text_input_change():
            """엔터키로 메시지 전송"""
            user = UserManager.get_user_by_id(st.session_state.chat_user_id)
            if st.session_state.user_input:
                handle_user_message(st.session_state.user_input, user)
                st.session_state.clear_input_after_send = True
                st.rerun()
        
        user_input = st.text_input(
            "메시지 입력",
            value=st.session_state.user_input,
            key="user_input",
            placeholder="여기에 입력하거나 음성으로 말씀해주세요...",
            label_visibility="collapsed",
            on_change=on_text_input_change
        )
    
    with col2:
        send_button = st.button("전송", use_container_width=True, type="primary")
    
    if send_button and user_input:
        handle_user_message(user_input, user)
        st.session_state.clear_input_after_send = True
        st.rerun()
    
    # 대화 종료 버튼
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 대화 저장 후 종료", use_container_width=True, type="secondary"):
            # 전체 메시지 조회
            messages = ChatManager.get_messages(st.session_state.chat_conversation_id)
            summary_result = create_session_summary(
                st.session_state.chat_conversation_id,
                [{
                    'role': msg['speaker'],
                    'content': msg['content']
                } for msg in messages]
            )

            # 요약 결과를 DB에 저장
            if summary_result:
                people = summary_result.get('people', [])
                next_topics = summary_result.get('next_topics', [])
                HistoryManager.create_summary(
                    st.session_state.chat_conversation_id,
                    ai_summary=st.session_state.chat_summary or '대화가 요약되었습니다.',
                    mentioned_people=', '.join(people) if people else None,
                    main_topics=', '.join(next_topics) if next_topics else None,
                    emotional_tone=None,
                    suggested_questions='; '.join(next_topics) if next_topics else None
                )

            ChatManager.end_conversation(st.session_state.chat_conversation_id)
            st.success("✅ 대화가 저장되었습니다!")
            st.balloons()
            
            # 세션 초기화
            st.session_state.chat_user_id = None
            st.session_state.chat_conversation_id = None
            st.session_state.chat_messages = []
            st.session_state.chat_api_messages = []
            st.session_state.chat_summary = None
            st.session_state.last_ai_audio = None
            st.rerun()
    
    with col2:
        if st.button("📊 대화 요약 보기", use_container_width=True):
            st.switch_page("pages/4_오늘대화요약.py")


def handle_user_message(message: str, user: dict):
    """사용자 메시지 처리"""
    # 사용자 메시지 저장
    ChatManager.add_message(
        st.session_state.chat_conversation_id,
        'user',
        message
    )
    
    st.session_state.chat_messages.append({
        'speaker': 'user',
        'content': message,
        'timestamp': datetime.now()
    })
    
    # AI 응답 생성
    st.session_state.waiting_for_ai = True

    # 새 사용자 메시지를 API 메시지 기록에도 추가
    st.session_state.chat_api_messages.append({
        'speaker': 'user',
        'content': message
    })

    # 이전 대화 기록을 messages로 보내고, summary가 있으면 함께 전달
    ai_result = generate_ai_response(
        message,
        user['id'],
        st.session_state.chat_summary,
        st.session_state.chat_api_messages
    )

    ai_response = ai_result.get('answer', '죄송합니다. 응답을 생성할 수 없습니다.')
    new_summary = ai_result.get('summary')

    # 대화 저장
    ChatManager.add_message(
        st.session_state.chat_conversation_id,
        'ai',
        ai_response
    )
    
    st.session_state.chat_messages.append({
        'speaker': 'ai',
        'content': ai_response,
        'timestamp': datetime.now()
    })

    # AI TTS 생성
    ai_audio = text_to_speech(ai_response)
    if ai_audio:
        st.session_state.last_ai_audio = ai_audio

    if new_summary:
        st.session_state.chat_summary = new_summary
        st.session_state.chat_api_messages = []
    else:
        st.session_state.chat_api_messages.append({
            'speaker': 'assistant',
            'content': ai_response
        })

    st.session_state.waiting_for_ai = False


def main():
    """메인 함수"""
    init_session_state()
    
    # 헤더
    st.markdown("""
        <div style="background-color: #FFF8DC; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1>💬 AI 대화</h1>
            <p>편안하게 추억을 이야기해보세요</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 대상자가 선택되지 않았으면 선택 화면
    if not st.session_state.chat_user_id or not st.session_state.chat_conversation_id:
        show_user_selector()
    else:
        show_chat_interface()
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 💬 AI 대화")
        st.markdown("---")

        st.info("""
            **💡 대화 팁**
            
            - 편안한 마음으로 자유롭게 이야기하세요
            - 과거의 즐거웠던 기억을 떠올려보세요
            - AI가 질문하면 천천히 답해주세요
            - 언제든지 대화를 멈추고 쉴 수 있습니다
        """)
        
        if st.session_state.chat_conversation_id:
            st.markdown("---")
            st.warning("💾 대화 중입니다. 종료 버튼을 눌러 저장하세요.")


if __name__ == "__main__":
    main()
