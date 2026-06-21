"""
오늘 대화 요약 페이지
오늘의 대화 통계 및 요약 정보
"""

import streamlit as st
from datetime import datetime, timedelta
import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_user import UserManager
from database.db_history import HistoryManager
from database.db_chat import ChatManager

# 페이지 설정
st.set_page_config(
    page_title="오늘 대화 요약 - 기억상자 AI",
    page_icon="📊",
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
    
    /* 페이지 헤더 */
    .page-header {
        background: linear-gradient(135deg, #F5F5DC 0%, #E8DCC4 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.1);
    }
    
    .page-header h1 {
        color: #8B4513;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    .page-header h2 {
        color: #D2691E;
        font-size: 1.5rem;
    }
    
    /* 요약 카드 */
    .summary-card {
        background-color: #FFF;
        padding: 2rem;
        border-radius: 18px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.1);
        border: 2px solid #E8DCC4;
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5F5DC 100%);
        padding: 2rem;
        border-radius: 18px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 3px 12px rgba(139, 69, 19, 0.12);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(139, 69, 19, 0.2);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: bold;
        color: #D2691E;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1.1rem;
        color: #666;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* 주제 태그 */
    .topic-tag {
        display: inline-block;
        background: linear-gradient(135deg, #F5F5DC 0%, #E8DCC4 100%);
        padding: 0.7rem 1.3rem;
        border-radius: 20px;
        margin: 0.4rem;
        font-size: 1rem;
        border: 2px solid #D2691E;
        font-weight: 600;
        color: #8B4513;
        transition: all 0.3s ease;
    }
    
    .topic-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(139, 69, 19, 0.2);
    }
    
    /* AI 요약 박스 */
    .ai-summary-box {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5F5DC 100%);
        padding: 2rem;
        border-radius: 18px;
        border-left: 6px solid #D2691E;
        margin: 1.5rem 0;
        box-shadow: 0 3px 12px rgba(139, 69, 19, 0.1);
    }
    
    /* 대화 미리보기 */
    .conversation-preview {
        background-color: #FAFAF0;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.7rem 0;
        border-left: 4px solid #D2691E;
    }
    
    /* 제안 박스 */
    .suggestion-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 1.5rem 0;
        border-left: 6px solid #4CAF50;
        box-shadow: 0 3px 12px rgba(76, 175, 80, 0.15);
    }
    
    .suggestion-box h4 {
        color: #2E7D32;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    /* 버튼 */
    .stButton>button {
        background-color: #D2B48C;
        color: #333 !important;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.8rem;
        font-size: 1rem;
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
    
    /* 셀렉트박스 - 모든 상태에 강제 적용 */
    .stSelectbox label {
        color: #333 !important;
        font-weight: 600 !important;
    }

    .stSelectbox > div > div {
        background-color: white !important;
        max-width: 400px !important;
    }

    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #333 !important;
        max-width: 400px !important;
    }

    .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
        max-width: 400px !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #D2691E !important;
        max-width: 400px !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div:hover {
        border-color: #8B4513 !important;
    }
    
    .stSelectbox [data-baseweb="select"] input {
        color: #333 !important;
        background-color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] svg {
        color: #333 !important;
        fill: #333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] span {
        color: #333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] div[data-testid="stMarkdownContainer"] {
        color: #333 !important;
    }
    
    /* 드롭다운 리스트 */
    .stSelectbox [role="listbox"] {
        background-color: white !important;
    }
    
    .stSelectbox [role="option"] {
        color: #333 !important;
        background-color: white !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: #F5F5DC !important;
        color: #333 !important;
    }
    
    /* 전역 셀렉트박스 스타일 강제 */
    [data-baseweb="select"] * {
        background-color: white !important;
        color: #333 !important;
    }
    
    [data-baseweb="popover"] {
        background-color: white !important;
    }
    
    [data-baseweb="popover"] * {
        background-color: white !important;
        color: #333 !important;
    }
    
    [data-baseweb="menu"] {
        background-color: white !important;
    }
    
    [data-baseweb="menu"] * {
        background-color: white !important;
        color: #333 !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #F5F5DC !important;
    }
    
    /* placeholder 텍스트도 어둡게 */
    ::placeholder {
        color: #666 !important;
        opacity: 1 !important;
    }
    
    /* 선택된 값 강제 스타일 */
    [data-baseweb="select"] [aria-selected="true"] {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background-color: #F5F5DC;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """세션 상태 초기화"""
    if 'summary_user_id' not in st.session_state:
        st.session_state.summary_user_id = None


def format_duration(seconds):
    """초를 분:초 형식으로 변환"""
    if not seconds:
        return "0분"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    
    if hours > 0:
        return f"{hours}시간 {minutes}분"
    else:
        return f"{minutes}분"


def show_today_summary(user_id: int):
    """오늘의 대화 요약"""
    
    user = UserManager.get_user_by_id(user_id)
    if not user:
        st.error("대상자 정보를 불러올 수 없습니다.")
        return
    
    # 오늘의 대화 조회
    today_conversations = HistoryManager.get_today_conversations(user_id)
    
    if not today_conversations:
        st.markdown("""
            <div class="summary-card" style="text-align: center; padding: 3rem;">
                <h2>📭 오늘은 아직 대화가 없습니다</h2>
                <p style="font-size: 1.2rem; color: #666; margin-top: 1rem;">
                    {name}님과 함께 추억을 나눠보세요
                </p>
            </div>
        """.format(name=user['name']), unsafe_allow_html=True)
        
        if st.button("💬 대화 시작하기", type="primary", use_container_width=True):
            st.switch_page("pages/2_AI대화.py")
        return
    
    # 통계 계산
    total_messages = sum(conv['message_count'] for conv in today_conversations)
    total_duration = sum(conv['duration'] or 0 for conv in today_conversations)
    completed_count = len([c for c in today_conversations if c['status'] == '완료'])
    
    # 헤더
    st.markdown(f"""
        <div class="page-header">
            <h1>📊 오늘 대화 요약</h1>
            <h2>{user['name']}님의 {datetime.now().strftime('%Y년 %m월 %d일')} 대화</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 주요 통계
    st.markdown("### 📈 오늘의 대화 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(today_conversations)}</div>
                <div class="metric-label">번</div>
                <p>대화 횟수</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{format_duration(total_duration)}</div>
                <div class="metric-label"></div>
                <p>총 대화 시간</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_messages}</div>
                <div class="metric-label">개</div>
                <p>주고받은 메시지</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{completed_count}</div>
                <div class="metric-label">회</div>
                <p>완료된 대화</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 각 대화별 요약
    st.markdown("### 💬 대화 내역")
    
    for idx, conv in enumerate(today_conversations, 1):
        with st.expander(
            f"🕐 {conv['start_time'].strftime('%H시 %M분')} 대화 "
            f"({conv['message_count']}개 메시지, {format_duration(conv['duration'])})"
        ):
            # 대화 상세 정보
            detail = HistoryManager.get_conversation_detail(conv['id'])
            
            if detail and detail['messages']:
                # 대화 미리보기 (처음 3개 메시지)
                st.markdown("#### 대화 시작 부분")
                
                for msg in detail['messages'][:3]:
                    speaker_emoji = "👤" if msg['speaker'] == 'user' else "🤖"
                    speaker_name = user['name'] if msg['speaker'] == 'user' else "AI"
                    
                    st.markdown(f"""
                        <div class="conversation-preview">
                            <strong>{speaker_emoji} {speaker_name}</strong>
                            <p>{msg['content']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                if len(detail['messages']) > 3:
                    st.caption(f"... 외 {len(detail['messages']) - 3}개 메시지 더 보기")
                
                # 요약 정보
                summary = HistoryManager.get_summary(conv['id'])
                
                if summary:
                    st.markdown("---")
                    st.markdown("#### 📝 AI 요약")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if summary['mentioned_people']:
                            st.markdown("**👥 언급된 인물**")
                            st.info(summary['mentioned_people'])
                        
                        if summary['main_topics']:
                            st.markdown("**🏷️ 주요 주제**")
                            topics = summary['main_topics'].split(',')
                            for topic in topics[:5]:  # 최대 5개만
                                st.markdown(f'<span class="topic-tag">{topic.strip()}</span>', unsafe_allow_html=True)
                    
                    with col2:
                        if summary['emotional_tone']:
                            st.markdown("**😊 감정 반응**")
                            st.info(summary['emotional_tone'])
                        
                        if summary['ai_summary']:
                            st.markdown("**📋 전체 요약**")
                            st.success(summary['ai_summary'])
                else:
                    st.info("요약이 아직 생성되지 않았습니다.")
                
                # 전체 대화 보기 버튼
                if st.button(f"전체 대화 보기", key=f"view_full_{conv['id']}", use_container_width=True):
                    st.session_state.selected_conversation_id = conv['id']
                    st.switch_page("pages/3_이전대화기록.py")
    
    st.markdown("---")
    
    # 종합 요약 섹션
    st.markdown("### 📊 오늘의 종합 요약")
    
    # 모든 요약 수집
    all_topics = []
    all_people = []
    all_emotions = []
    
    for conv in today_conversations:
        summary = HistoryManager.get_summary(conv['id'])
        if summary:
            if summary['main_topics']:
                all_topics.extend([t.strip() for t in summary['main_topics'].split(',')])
            if summary['mentioned_people']:
                all_people.extend([p.strip() for p in summary['mentioned_people'].split(',')])
            if summary['emotional_tone']:
                all_emotions.append(summary['emotional_tone'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="summary-card">
                <h3>🏷️ 오늘 나눈 주제</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if all_topics:
            # 중복 제거 및 빈도 계산
            from collections import Counter
            topic_counts = Counter(all_topics)
            top_topics = topic_counts.most_common(5)
            
            for topic, count in top_topics:
                st.markdown(f'<span class="topic-tag">{topic} ({count}회)</span>', unsafe_allow_html=True)
        else:
            st.caption("주제 정보가 없습니다.")
    
    with col2:
        st.markdown("""
            <div class="summary-card">
                <h3>👥 언급된 인물들</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if all_people:
            # 중복 제거
            unique_people = list(set(all_people))[:5]
            for person in unique_people:
                st.markdown(f"- {person}")
        else:
            st.caption("언급된 인물 정보가 없습니다.")
    
    # 다음 대화 제안
    st.markdown("---")
    st.markdown("### 💡 다음에 이야기할 주제")
    
    # 최근 대화의 제안 질문 수집
    suggestions = []
    for conv in today_conversations:
        summary = HistoryManager.get_summary(conv['id'])
        if summary and summary['suggested_questions']:
            suggestions.append(summary['suggested_questions'])
    
    if suggestions:
        st.markdown(f"""
            <div class="suggestion-box">
                <h4>🌟 AI가 제안하는 다음 대화 주제</h4>
                <p>{suggestions[0]}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # 기본 제안
        st.markdown("""
            <div class="suggestion-box">
                <h4>🌟 이런 주제는 어떠세요?</h4>
                <ul>
                    <li>어렸을 때 가장 기억에 남는 명절은 언제였나요?</li>
                    <li>처음 직장에 다니실 때 어떤 기분이셨나요?</li>
                    <li>가족들과 함께 갔던 여행 중 가장 즐거웠던 곳은 어디인가요?</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # 액션 버튼
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 새 대화 시작하기", use_container_width=True, type="primary"):
            st.switch_page("pages/2_AI대화.py")
    
    with col2:
        if st.button("📋 전체 대화 기록 보기", use_container_width=True):
            st.switch_page("pages/3_이전대화기록.py")
    
    with col3:
        if st.button("📥 오늘 대화 내보내기", use_container_width=True):
            # 오늘의 전체 대화 내보내기
            export_text = f"=== {user['name']}님의 {datetime.now().strftime('%Y년 %m월 %d일')} 대화 요약 ===\n\n"
            export_text += f"총 대화 횟수: {len(today_conversations)}회\n"
            export_text += f"총 대화 시간: {format_duration(total_duration)}\n"
            export_text += f"총 메시지: {total_messages}개\n\n"
            export_text += "=" * 50 + "\n\n"
            
            for idx, conv in enumerate(today_conversations, 1):
                detail = HistoryManager.get_conversation_detail(conv['id'])
                if detail:
                    export_text += f"\n[대화 {idx}] {conv['start_time'].strftime('%H:%M')}\n"
                    export_text += "-" * 50 + "\n"
                    
                    for msg in detail['messages']:
                        speaker = user['name'] if msg['speaker'] == 'user' else 'AI'
                        timestamp = msg['timestamp'].strftime('%H:%M')
                        export_text += f"[{timestamp}] {speaker}: {msg['content']}\n"
                    
                    export_text += "\n"
            
            st.download_button(
                label="💾 TXT 파일로 다운로드",
                data=export_text,
                file_name=f"{user['name']}_대화요약_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )


def show_weekly_comparison(user_id: int):
    """주간 비교 통계"""
    st.markdown("### 📅 최근 7일 비교")
    
    # 최근 7일 데이터 수집
    daily_stats = []
    
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        convs = HistoryManager.get_conversations_by_date(user_id, date)
        
        total_messages = sum(c['message_count'] for c in convs)
        total_duration = sum(c['duration'] or 0 for c in convs)
        
        daily_stats.append({
            'date': date.strftime('%m/%d'),
            'count': len(convs),
            'messages': total_messages,
            'duration': total_duration
        })
    
    daily_stats.reverse()  # 날짜 순서대로
    
    # 차트 데이터
    import pandas as pd
    
    df = pd.DataFrame(daily_stats)
    
    if df['count'].sum() > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 일별 대화 횟수")
            st.bar_chart(df.set_index('date')['count'])
        
        with col2:
            st.markdown("#### 일별 메시지 수")
            st.bar_chart(df.set_index('date')['messages'])
    else:
        st.info("최근 7일간 대화 기록이 없습니다.")


def main():
    """메인 함수"""
    init_session_state()
    
    # 대상자 선택
    users = UserManager.get_all_users()
    
    if not users:
        st.warning("등록된 대상자가 없습니다.")
        if st.button("➕ 대상자 등록하러 가기"):
            st.switch_page("pages/1_대상정보.py")
        return
    
    # 대상자 선택
    user_options = {f"{user['name']} ({user['birth_year']}년생)" if user['birth_year'] 
                   else user['name']: user['id'] for user in users}
    
    selected_name = st.selectbox(
        "👤 대상자 선택",
        options=list(user_options.keys())
    )
    
    st.session_state.summary_user_id = user_options[selected_name]
    
    st.markdown("---")
    
    # 탭 구성
    tab1, tab2 = st.tabs(["📊 오늘의 요약", "📅 주간 비교"])
    
    with tab1:
        show_today_summary(st.session_state.summary_user_id)
    
    with tab2:
        show_weekly_comparison(st.session_state.summary_user_id)
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 📊 대화 요약")
        st.markdown("---")

        st.info("""
            **💡 요약 활용 팁**
            
            - 오늘의 대화를 되돌아보세요
            - 자주 나오는 주제를 파악하세요
            - 제안된 질문으로 다음 대화를 준비하세요
            - 가족과 요약을 공유하세요
        """)


if __name__ == "__main__":
    main()
