import streamlit as st
from datetime import datetime
import os
import requests
import json

st.set_page_config(page_title="AI 대화 - 기억상자 AI", layout="wide")

# API 주소 설정 (끝에 슬래시를 제거하여 중복 방지)
API_URL = "https://4a570ef2.service.gcube.ai:24999".strip("/")

def init_session_state():
    if 'users' not in st.session_state: st.session_state.users = []
    if 'conversations' not in st.session_state: st.session_state.conversations = []
    if 'messages' not in st.session_state: st.session_state.messages = []
    if 'chat_user_id' not in st.session_state: st.session_state.chat_user_id = None
    if 'chat_conversation_id' not in st.session_state: st.session_state.chat_conversation_id = None
    if 'chat_summary' not in st.session_state: st.session_state.chat_summary = None

def generate_ai_response(user_message, user_id, chat_history):
    """
    FastAPI 서버에 대화 요청
    """
    # 백엔드가 기대하는 데이터 구조로 변환
    formatted_history = []
    for m in chat_history:
        role = "assistant" if m['role'] == "ai" else "user"
        formatted_history.append({"role": role, "content": m['content']})

    payload = {
        "query": user_message,
        "messages": formatted_history,
        "user_id": user_id,
        "summary": st.session_state.get('chat_summary', "")
    }

    try:
        # 타임아웃을 60초로 대폭 늘림 (AI 생성 시간 고려)
        # 경로를 /chat/ 또는 /chat으로 백엔드 설정에 맞게 조정
        response = requests.post(
            f"{API_URL}/chat/", 
            json=payload, 
            timeout=60,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            # 서버에서 summary를 돌려주면 저장
            if 'summary' in result:
                st.session_state.chat_summary = result['summary']
            return result.get("answer")
        else:
            # 에러 발생 시 상세 정보 출력 (디버깅용)
            st.error(f"서버 에러 발생 (코드: {response.status_code})")
            st.write(response.text) # 서버가 보내는 구체적인 에러 메시지 확인
            return None
            
    except requests.exceptions.Timeout:
        st.error("서버 응답 시간이 초과되었습니다. (AI가 생각하는데 시간이 오래 걸리고 있습니다.)")
    except Exception as e:
        st.error(f"연결 오류: {str(e)}")
    
    return "어르신, 잠시 통신이 원활하지 않아요. 다시 말씀해 주시겠어요?"

def add_message(c_id, speaker, content):
    st.session_state.messages.append({
        "conversation_id": c_id,
        "speaker": speaker,
        "content": content,
        "timestamp": datetime.now()
    })
    for c in st.session_state.conversations:
        if c['id'] == c_id:
            c['message_count'] = c.get('message_count', 0) + 1

def main():
    init_session_state()
    
    if st.session_state.chat_user_id is None:
        st.title("💬 대화 시작하기")
        if not st.session_state.users:
            st.warning("먼저 '대상정보' 페이지에서 어르신을 등록해주세요.")
            return
        
        user_map = {u['name']: u for u in st.session_state.users}
        selected_name = st.selectbox("어르신을 선택해주세요", list(user_map.keys()))
        
        if st.button("대화 시작", type="primary"):
            selected_user = user_map[selected_name]
            c_id = int(datetime.now().timestamp())
            
            st.session_state.chat_user_id = selected_user['id']
            st.session_state.chat_conversation_id = c_id
            
            st.session_state.conversations.append({
                "id": c_id,
                "user_id": selected_user['id'],
                "user_name": selected_name,
                "start_time": datetime.now(),
                "message_count": 0
            })
            
            welcome_msg = f"안녕하세요, {selected_name}님! 오늘 하루는 어떠셨나요?"
            add_message(c_id, "ai", welcome_msg)
            st.rerun()
    else:
        user = next(u for u in st.session_state.users if u['id'] == st.session_state.chat_user_id)
        st.title(f"💬 {user['name']}님과 대화 중")
        
        c_id = st.session_state.chat_conversation_id
        # 현재 세션의 메시지만 필터링
        msgs = [m for m in st.session_state.messages if m['conversation_id'] == c_id]
        
        # 채팅 로그 표시
        for m in msgs:
            with st.chat_message(m['speaker']):
                st.write(m['content'])

        # 사용자 입력
        u_input = st.chat_input("여기에 말씀해 주세요...")
        if u_input:
            # 1. 사용자 메시지 즉시 표시 및 저장
            add_message(c_id, "user", u_input)
            
            # 2. AI 답변 생성
            history = [{"role": m['speaker'], "content": m['content']} for m in msgs]
            with st.chat_message("ai"):
                with st.spinner("생각 중..."):
                    ans = generate_ai_response(u_input, user['id'], history)
                    if ans:
                        st.write(ans)
                        add_message(c_id, "ai", ans)
                        st.rerun()

        if st.button("💾 대화 종료"):
            st.session_state.chat_user_id = None
            st.session_state.chat_conversation_id = None
            st.rerun()

if __name__ == "__main__":
    main()