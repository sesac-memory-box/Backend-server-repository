import streamlit as st
from datetime import datetime

st.set_page_config(page_title="오늘 대화 요약 - 기억상자 AI", layout="wide")

def main():
    st.title("📊 오늘 대화 요약")
    
    if 'conversations' not in st.session_state:
        st.info("오늘 진행된 대화가 없습니다.")
        return

    today = datetime.now().date()
    # 오늘 날짜에 해당하는 대화만 필터링
    today_convs = [c for c in st.session_state.conversations if c['start_time'].date() == today]

    if not today_convs:
        st.info("오늘은 아직 대화 기록이 없습니다.")
        return

    st.write(f"### {today.strftime('%Y년 %m월 %d일')} 리포트")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("오늘 대화 횟수", f"{len(today_convs)}회")
    with col2:
        # get('message_count', 0)으로 에러 방지
        total_msgs = sum(c.get('message_count', 0) for c in today_convs)
        st.metric("오늘 주고받은 메시지", f"{total_msgs}개")

    st.divider()
    st.write("#### 📝 대화별 요약 (임시)")
    for c in today_convs:
        st.write(f"- **{c['start_time'].strftime('%H:%M')} 대화:** 메시지 {c.get('message_count', 0)}개 주고받음 (상태: {c.get('status', '종료')})")

if __name__ == "__main__":
    main()