import streamlit as st

st.set_page_config(page_title="이전 대화 기록 - 기억상자 AI", layout="wide")

def main():
    st.title("📋 이전 대화 기록")
    
    if 'conversations' not in st.session_state or not st.session_state.conversations:
        st.info("아직 기록된 대화가 없습니다.")
        return

    # 최신 대화가 위로 오도록 정렬
    for conv in reversed(st.session_state.conversations):
        # 데이터가 없을 경우를 대비해 get() 사용
        msg_count = conv.get('message_count', 0)
        user_name = conv.get('user_name', '알 수 없음')
        time_str = conv['start_time'].strftime('%Y-%m-%d %H:%M')
        
        with st.expander(f"📅 {time_str} | 대상: {user_name} | 메시지 {msg_count}개"):
            msgs = [m for m in st.session_state.get('messages', []) if m['conversation_id'] == conv['id']]
            if not msgs:
                st.write("내역이 없습니다.")
            for m in msgs:
                speaker_label = "🤖 AI" if m['speaker'] == "ai" else f"👤 {user_name}"
                st.write(f"**{speaker_label}:** {m['content']}")

if __name__ == "__main__":
    main()