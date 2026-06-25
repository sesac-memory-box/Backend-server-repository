import streamlit as st
from datetime import datetime
import os
import requests
import json
import sounddevice as sd
from scipy.io import wavfile
import numpy as np
import io

st.set_page_config(page_title="AI 대화 - 기억상자 AI", layout="wide")

# API 주소 설정
API_URL = "https://4a570ef2.service.gcube.ai:24999".strip("/")

def init_session_state():
    """세션 상태 초기화 및 데이터 구조 정의"""
    if 'users' not in st.session_state: st.session_state.users = []
    if 'conversations' not in st.session_state: st.session_state.conversations = []
    if 'messages' not in st.session_state: st.session_state.messages = []
    if 'chat_user_id' not in st.session_state: st.session_state.chat_user_id = None
    if 'chat_conversation_id' not in st.session_state: st.session_state.chat_conversation_id = None
    if 'chat_summary' not in st.session_state: st.session_state.chat_summary = ""
    if 'last_ai_audio' not in st.session_state: st.session_state.last_ai_audio = None

# --- 음성 관련 기능 ---

def record_audio(duration=5, fs=16000):
    try:
        st.info(f"🎤 {duration}초 동안 말씀해주세요...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        buffer = io.BytesIO()
        wavfile.write(buffer, fs, recording)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"마이크 녹음 실패: {e}")
        return None

def speech_to_text(audio_buffer):
    if audio_buffer is None: return None
    try:
        files = {"audio": ("recording.wav", audio_buffer, "audio/wav")}
        response = requests.post(f"{API_URL}/stt/", files=files, timeout=30)
        if response.status_code == 200:
            return response.json().get("transcript")
    except Exception as e:
        st.error(f"STT 인식 오류: {e}")
    return None

def text_to_speech(text):
    try:
        payload = {"text": text, "voice": "alloy"}
        response = requests.post(f"{API_URL}/tts/", json=payload, timeout=30)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        st.error(f"TTS 합성 오류: {e}")
    return None

# --- 대화 로직 (에러 수정 지점) ---

def generate_ai_response(user_message, user_id, chat_messages):
    """
    chat_messages: st.session_state.messages에서 가져온 원본 메시지 리스트
    """
    formatted_history = []
    for m in chat_messages:
        # KeyError 방지를 위해 .get() 사용 및 키 이름 확인
        # 세션에 저장된 키는 'speaker'입니다.
        speaker = m.get('speaker', 'user')
        role = "assistant" if speaker == "ai" else "user"
        formatted_history.append({
            "role": role, 
            "content": m.get('content', '')
        })

    payload = {
        "query": user_message,
        "messages": formatted_history,
        "user_id": user_id,
        "summary": st.session_state.get('chat_summary', "")
    }

    try:
        response = requests.post(f"{API_URL}/chat/", json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if 'summary' in result:
                st.session_state.chat_summary = result['summary']
            return result.get("answer")
    except Exception as e:
        st.error(f"AI 응답 생성 실패: {str(e)}")
    
    return "어르신, 잠시 통신이 원활하지 않아요. 다시 말씀해 주시겠어요?"

def add_message(c_id, speaker, content):
    """메시지 저장 구조 통일"""
    st.session_state.messages.append({
        "conversation_id": c_id,
        "speaker": speaker, # 'ai' 또는 'user'
        "content": content,
        "timestamp": datetime.now()
    })

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
                "id": c_id, "user_id": selected_user['id'], 
                "user_name": selected_name, "start_time": datetime.now()
            })
            
            welcome_msg = f"안녕하세요, {selected_name}님! 오늘 하루는 어떠셨나요?"
            add_message(c_id, "ai", welcome_msg)
            
            # 음성 생성
            audio_data = text_to_speech(welcome_msg)
            if audio_data: st.session_state.last_ai_audio = audio_data
            st.rerun()
    else:
        user = next(u for u in st.session_state.users if u['id'] == st.session_state.chat_user_id)
        st.title(f"💬 {user['name']}님과 대화 중")
        c_id = st.session_state.chat_conversation_id
        
        # 음성 자동 재생
        if st.session_state.last_ai_audio:
            st.audio(st.session_state.last_ai_audio, format="audio/wav", autoplay=True)
            st.session_state.last_ai_audio = None

        # 현재 대화 세션 메시지만 필터링
        msgs = [m for m in st.session_state.messages if m.get('conversation_id') == c_id]
        
        for m in msgs:
            with st.chat_message(m.get('speaker', 'user')):
                st.write(m.get('content', ''))

        st.divider()
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("🎤 말씀하기 (5초)", use_container_width=True):
                audio_buffer = record_audio(duration=5)
                transcript = speech_to_text(audio_buffer)
                if transcript:
                    st.session_state.voice_input = transcript
                    st.rerun()

        with col2:
            default_text = st.session_state.get('voice_input', "")
            # 음성 입력이 있으면 chat_input 대신 임시로 보여주거나 처리
            if default_text:
                st.info(f"인식된 내용: {default_text}")
                u_input = default_text
                del st.session_state.voice_input
            else:
                u_input = st.chat_input("여기에 말씀해주시거나 입력해주세요")

        if u_input:
            # 1. 사용자 메시지 저장
            add_message(c_id, "user", u_input)
            
            # 2. AI 응답 생성 (msgs 리스트를 직접 전달)
            with st.spinner("AI가 생각 중..."):
                ans = generate_ai_response(u_input, user['id'], msgs)
                if ans:
                    # 3. AI 메시지 저장
                    add_message(c_id, "ai", ans)
                    # 4. 음성 합성
                    audio_data = text_to_speech(ans)
                    if audio_data:
                        st.session_state.last_ai_audio = audio_data
                    st.rerun()

        if st.button("💾 대화 종료"):
            st.session_state.chat_user_id = None
            st.session_state.chat_conversation_id = None
            st.session_state.last_ai_audio = None
            st.rerun()

if __name__ == "__main__":
    main()