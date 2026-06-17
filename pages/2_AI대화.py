"""
AI 대화 페이지
AI와 회상 대화하기
"""

import streamlit as st
from datetime import datetime
import os
import sys

# 프로젝트 루트를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_user import UserManager
from database.db_chat import ChatManager
from database.db_history import HistoryManager

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
        background-color: #D2691E;
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #A0522D;
        color: white !important;
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
    
    /* 입력 필드 */
    .stTextInput>div>div>input {
        border: 2px solid #E8DCC4;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #D2691E;
        box-shadow: 0 0 0 3px rgba(210, 105, 30, 0.1);
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
    
    if 'waiting_for_ai' not in st.session_state:
        st.session_state.waiting_for_ai = False


def generate_ai_response(user_message: str, user_info: dict, conversation_history: list) -> str:
    """
    AI 응답 생성 (OpenAI API 사용)
    실제 구현 시 OpenAI API를 호출하여 응답 생성
    
    Args:
        user_message: 사용자 메시지
        user_info: 대상자 정보
        conversation_history: 대화 히스토리
    
    Returns:
        str: AI 응답
    """
    # TODO: OpenAI API 연동
    # 여기서는 간단한 템플릿 응답을 반환
    
    # 환경변수에서 OpenAI API 키 확인
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        # API 키가 없을 때 샘플 응답
        sample_responses = [
            f"그렇군요! {user_info.get('name', '어르신')}께서 {user_message}라고 말씀하셨네요. 그 시절 어떤 냄새가 났나요?",
            f"정말 재미있는 이야기네요! 그때 누구와 함께 계셨나요?",
            f"아, 그 이야기를 들으니 그 시절이 떠오르시나요? 더 자세히 말씀해 주시겠어요?",
            f"그때는 정말 좋은 시절이었을 것 같아요. 어떤 기분이셨나요?",
        ]
        import random
        return random.choice(sample_responses)
    
    try:
        # OpenAI API 호출 (실제 구현)
        import openai
        openai.api_key = api_key
        
        # 시스템 프롬프트 구성
        system_prompt = f"""당신은 치매 어르신을 위한 친절한 대화 상대입니다.
        
대상자 정보:
- 이름: {user_info.get('name', '어르신')}
- 출생연도: {user_info.get('birth_year', '알 수 없음')}
- 과거 직업: {user_info.get('past_job', '알 수 없음')}
- 거주지역: {user_info.get('residence', '알 수 없음')}
- 좋아하는 음식: {user_info.get('favorite_food', '알 수 없음')}
- 추억의 장소: {user_info.get('memorable_place', '알 수 없음')}
- 좋아했던 노래/가수: {user_info.get('favorite_song', '알 수 없음')}

대화 원칙:
1. 과거의 구체적인 경험을 떠올리도록 감각 중심 질문을 합니다 (냄새, 소리, 촉감 등)
2. "그때 어땠나요?", "누구와 함께였나요?" 같은 열린 질문을 사용합니다
3. 짧고 간결하게 2-3문장으로 응답합니다
4. 공감하고 격려하는 톤을 유지합니다
5. 대상자의 과거 정보를 자연스럽게 대화에 활용합니다
"""
        
        # 대화 히스토리 구성
        messages = [{"role": "system", "content": system_prompt}]
        
        # 최근 5개 메시지만 포함
        for msg in conversation_history[-5:]:
            role = "user" if msg['speaker'] == 'user' else "assistant"
            messages.append({"role": role, "content": msg['content']})
        
        messages.append({"role": "user", "content": user_message})
        
        # API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"AI 응답 생성 오류: {e}")
        return f"죄송합니다. 지금은 응답을 생성할 수 없습니다. ({str(e)})"


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
    
    selected_name = st.selectbox(
        "대상자 선택",
        options=list(user_options.keys()),
        key="user_selector"
    )
    
    if st.button("대화 시작하기", type="primary", use_container_width=True):
        user_id = user_options[selected_name]
        st.session_state.chat_user_id = user_id
        
        # 새 대화 세션 생성
        result = ChatManager.create_conversation(user_id)
        if result:
            conversation_id, session_id = result
            st.session_state.chat_conversation_id = conversation_id
            st.session_state.chat_messages = []
            
            # 환영 메시지 추가
            user = UserManager.get_user_by_id(user_id)
            welcome_msg = f"안녕하세요, {user['name']}님! 😊 오늘은 어떤 추억을 이야기할까요?"
            
            ChatManager.add_message(conversation_id, 'ai', welcome_msg)
            st.session_state.chat_messages.append({
                'speaker': 'ai',
                'content': welcome_msg,
                'timestamp': datetime.now()
            })
            
            st.rerun()
        else:
            st.error("대화 세션 생성에 실패했습니다.")
    
    return False


def show_chat_interface():
    """채팅 인터페이스"""
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
    
    # AI가 응답 중일 때
    if st.session_state.waiting_for_ai:
        st.info("🤔 AI가 생각하고 있습니다...")
    
    # 제안 질문 (대화가 시작된 경우)
    if len(st.session_state.chat_messages) > 1:
        st.markdown("#### 💡 이런 질문은 어떠세요?")
        
        suggestions = [
            "국말이 제일 맛있던 음식점은 어디였나요?",
            "친구들과 즐겨 했던 놀이가 있나요?",
            "어렸을 때 꿈은 무엇이었나요?"
        ]
        
        cols = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                    handle_user_message(suggestion, user)
    
    # 메시지 입력
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "메시지 입력",
            key="user_input",
            placeholder="여기에 입력하거나 음성으로 말씀해주세요...",
            label_visibility="collapsed"
        )
    
    with col2:
        col_send, col_mic = st.columns(2)
        with col_send:
            send_button = st.button("전송", use_container_width=True, type="primary")
        with col_mic:
            mic_button = st.button("🎤", use_container_width=True)
    
    if send_button and user_input:
        handle_user_message(user_input, user)
        st.rerun()
    
    if mic_button:
        st.info("🎤 음성 인식 기능은 개발 중입니다. 텍스트로 입력해주세요.")
    
    # 대화 종료 버튼
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 대화 저장 후 종료", use_container_width=True, type="secondary"):
            ChatManager.end_conversation(st.session_state.chat_conversation_id)
            st.success("✅ 대화가 저장되었습니다!")
            st.balloons()
            
            # 세션 초기화
            st.session_state.chat_user_id = None
            st.session_state.chat_conversation_id = None
            st.session_state.chat_messages = []
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
    
    ai_response = generate_ai_response(
        message,
        user,
        st.session_state.chat_messages
    )
    
    # AI 응답 저장
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
        
        if st.button("🏠 메인으로", use_container_width=True):
            st.switch_page("app.py")
        
        if st.button("👤 대상정보", use_container_width=True):
            st.switch_page("pages/1_대상정보.py")
        
        if st.button("📋 대화 기록", use_container_width=True):
            st.switch_page("pages/3_이전대화기록.py")
        
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
