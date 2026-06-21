"""
이전 대화 기록 페이지
과거 대화 내역 조회 및 상세보기
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
    page_title="이전 대화 기록 - 기억상자 AI",
    page_icon="📋",
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
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.1);
    }
    
    .page-header h1 {
        color: #8B4513;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* 대화 카드 */
    .conversation-card {
        background-color: #FFF;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #D2691E;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(139, 69, 19, 0.08);
    }
    
    .conversation-card:hover {
        box-shadow: 0 6px 15px rgba(139, 69, 19, 0.15);
        transform: translateY(-3px);
        border-left-width: 8px;
    }
    
    .conversation-card h4 {
        color: #8B4513;
        margin-bottom: 0.8rem;
    }
    
    /* 태그 */
    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #F5F5DC 0%, #E8DCC4 100%);
        padding: 0.4rem 1rem;
        border-radius: 15px;
        margin: 0.3rem;
        font-size: 0.9rem;
        border: 1px solid #D2691E;
    }
    
    /* 메시지 상세 */
    .message-detail {
        background-color: #FAFAF0;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.7rem 0;
        border-left: 3px solid #E8DCC4;
    }
    
    .message-user {
        border-left-color: #8B4513;
    }
    
    .message-ai {
        border-left-color: #D2691E;
    }
    
    /* 통계 박스 */
    .stats-box {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5F5DC 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(139, 69, 19, 0.1);
    }
    
    .stats-box h2 {
        color: #D2691E;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* 필터 섹션 */
    .filter-section {
        background-color: #F5F5DC;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* 버튼 */
    .stButton>button {
        background-color: #D2B48C;
        color: #333 !important;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
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
    }
    
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #D2691E !important;
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
    if 'history_user_id' not in st.session_state:
        st.session_state.history_user_id = None
    
    if 'selected_conversation_id' not in st.session_state:
        st.session_state.selected_conversation_id = None
    
    if 'date_filter' not in st.session_state:
        st.session_state.date_filter = 'all'


def format_duration(seconds):
    """초를 분:초 형식으로 변환"""
    if not seconds:
        return "0분 0초"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}분 {secs}초"


def show_conversation_list(user_id: int, date_filter: str = 'all'):
    """대화 목록 표시"""
    
    # 날짜 필터에 따라 대화 조회
    if date_filter == 'today':
        conversations = HistoryManager.get_today_conversations(user_id)
        st.markdown("### 📅 오늘의 대화")
    elif date_filter == 'week':
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        conversations = HistoryManager.get_conversations_by_date_range(user_id, start_date, end_date)
        st.markdown("### 📅 최근 7일 대화")
    elif date_filter == 'month':
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        conversations = HistoryManager.get_conversations_by_date_range(user_id, start_date, end_date)
        st.markdown("### 📅 최근 30일 대화")
    else:
        conversations = HistoryManager.get_user_conversations(user_id, limit=50)
        st.markdown("### 📅 전체 대화 기록")
    
    if not conversations:
        st.info("대화 기록이 없습니다. AI와 대화를 시작해보세요!")
        if st.button("💬 AI 대화 시작하기"):
            st.switch_page("pages/2_AI대화.py")
        return
    
    st.caption(f"총 {len(conversations)}개의 대화")
    
    # 대화 목록 표시
    for conv in conversations:
        with st.container():
            # 날짜 및 시간 표시
            date_str = conv['start_time'].strftime('%Y년 %m월 %d일')
            time_str = conv['start_time'].strftime('%H:%M')
            
            # 대화 카드
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                    <div class="conversation-card">
                        <h4>🗓️ {date_str} · {time_str} · {conv['status']}</h4>
                        <p>
                            <span class="tag">⏱️ {format_duration(conv['duration'])}</span>
                            <span class="tag">💬 {conv['message_count']}개 메시지</span>
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("상세보기", key=f"view_{conv['id']}", use_container_width=True):
                    st.session_state.selected_conversation_id = conv['id']
                    st.rerun()


def show_conversation_detail(conversation_id: int):
    """대화 상세 내용 표시"""
    
    # 대화 상세 정보 조회
    detail = HistoryManager.get_conversation_detail(conversation_id)
    
    if not detail:
        st.error("대화 정보를 불러올 수 없습니다.")
        return
    
    # 헤더
    col1, col2 = st.columns([3, 1])
    
    with col1:
        date_str = detail['start_time'].strftime('%Y년 %m월 %d일 %H:%M')
        st.markdown(f"### 📋 {date_str}의 대화")
        st.caption(f"👤 {detail['user_name']}님 · {detail['status']}")
    
    with col2:
        if st.button("⬅️ 목록으로", use_container_width=True):
            st.session_state.selected_conversation_id = None
            st.rerun()
    
    # 대화 통계
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stats-box">
                <h2>{detail['message_count']}</h2>
                <p>총 메시지</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        user_msg_count = len([m for m in detail['messages'] if m['speaker'] == 'user'])
        st.markdown(f"""
            <div class="stats-box">
                <h2>{user_msg_count}</h2>
                <p>사용자 메시지</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ai_msg_count = len([m for m in detail['messages'] if m['speaker'] == 'ai'])
        st.markdown(f"""
            <div class="stats-box">
                <h2>{ai_msg_count}</h2>
                <p>AI 메시지</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stats-box">
                <h2>{format_duration(detail['duration'])}</h2>
                <p>대화 시간</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 대화 내용
    st.markdown("### 💬 전체 대화")
    
    # 탭으로 보기 옵션 제공
    tab1, tab2 = st.tabs(["대화형 보기", "요약 보기"])
    
    with tab1:
        # 메시지 표시
        for msg in detail['messages']:
            timestamp = msg['timestamp'].strftime('%H:%M')
            
            if msg['speaker'] == 'user':
                st.markdown(f"""
                    <div class="message-detail message-user">
                        <strong>👤 {detail['user_name']}</strong> · {timestamp}
                        <p>{msg['content']}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="message-detail message-ai">
                        <strong>🤖 AI 상담사</strong> · {timestamp}
                        <p>{msg['content']}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # 요약 정보 조회
        summary = HistoryManager.get_summary(conversation_id)
        
        if summary:
            st.markdown("#### 📊 AI 생성 요약")
            if summary['ai_summary']:
                st.info(summary['ai_summary'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                if summary['mentioned_people']:
                    st.markdown("#### 👥 언급된 인물")
                    st.write(summary['mentioned_people'])
                
                if summary['main_topics']:
                    st.markdown("#### 🏷️ 주요 주제")
                    st.write(summary['main_topics'])
            
            with col2:
                if summary['emotional_tone']:
                    st.markdown("#### 😊 감정 반응")
                    st.write(summary['emotional_tone'])
                
                if summary['suggested_questions']:
                    st.markdown("#### 💡 다음 대화 제안")
                    st.write(summary['suggested_questions'])
        else:
            st.info("아직 요약이 생성되지 않았습니다.")
            if st.button("📊 요약 생성하기"):
                st.info("요약 생성 기능은 개발 중입니다.")
    
    # 액션 버튼
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 대화 내보내기", use_container_width=True):
            # 텍스트 파일로 내보내기
            export_text = f"대화 기록 - {date_str}\n"
            export_text += f"참여자: {detail['user_name']}\n"
            export_text += "=" * 50 + "\n\n"
            
            for msg in detail['messages']:
                speaker = detail['user_name'] if msg['speaker'] == 'user' else 'AI'
                timestamp = msg['timestamp'].strftime('%H:%M')
                export_text += f"[{timestamp}] {speaker}: {msg['content']}\n\n"
            
            st.download_button(
                label="💾 TXT 파일로 다운로드",
                data=export_text,
                file_name=f"대화기록_{detail['start_time'].strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("🗑️ 대화 삭제", use_container_width=True, type="secondary"):
            if st.session_state.get(f"confirm_delete_{conversation_id}", False):
                ChatManager.delete_conversation(conversation_id)
                st.success("대화가 삭제되었습니다.")
                st.session_state.selected_conversation_id = None
                st.rerun()
            else:
                st.session_state[f"confirm_delete_{conversation_id}"] = True
                st.warning("한 번 더 클릭하시면 삭제됩니다.")
    
    with col3:
        if st.button("📊 대화 요약 보기", use_container_width=True, type="primary"):
            st.switch_page("pages/4_오늘대화요약.py")


def show_statistics_dashboard(user_id: int):
    """통계 대시보드"""
    stats = HistoryManager.get_user_statistics(user_id)
    
    if not stats or stats['total_conversations'] == 0:
        st.info("아직 대화 통계가 없습니다.")
        return
    
    st.markdown("### 📊 대화 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 대화 수", f"{stats['total_conversations']}회")
    
    with col2:
        st.metric("총 메시지 수", f"{stats['total_messages']}개")
    
    with col3:
        avg_duration = int(stats['avg_duration']) if stats['avg_duration'] else 0
        st.metric("평균 대화 시간", format_duration(avg_duration))
    
    with col4:
        total_duration = int(stats['total_duration']) if stats['total_duration'] else 0
        st.metric("총 대화 시간", format_duration(total_duration))
    
    # 최근 주제
    st.markdown("### 🏷️ 최근 대화 주제")
    topics = HistoryManager.get_recent_topics(user_id, limit=5)
    
    if topics:
        for topic in topics:
            st.markdown(f"- {topic}")
    else:
        st.caption("아직 주제 정보가 없습니다.")


def main():
    """메인 함수"""
    init_session_state()
    
    # 헤더
    st.markdown("""
        <div class="page-header">
            <h1>📋 이전 대화 기록</h1>
            <p>과거의 소중한 대화를 다시 살펴보세요</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 대상자 선택
    users = UserManager.get_all_users()
    
    if not users:
        st.warning("등록된 대상자가 없습니다.")
        if st.button("➕ 대상자 등록하러 가기"):
            st.switch_page("pages/1_대상정보.py")
        return
    
    # 대상자 선택 드롭다운
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        user_options = {f"{user['name']} ({user['birth_year']}년생)" if user['birth_year'] 
                       else user['name']: user['id'] for user in users}
        
        selected_name = st.selectbox(
            "👤 대상자 선택",
            options=list(user_options.keys())
        )
        
        st.session_state.history_user_id = user_options[selected_name]
    
    with col2:
        # 날짜 필터
        date_filter = st.selectbox(
            "📅 기간 필터",
            options=['all', 'today', 'week', 'month'],
            format_func=lambda x: {
                'all': '전체',
                'today': '오늘',
                'week': '최근 7일',
                'month': '최근 30일'
            }[x]
        )
        st.session_state.date_filter = date_filter
    
    with col3:
        # 검색
        search_keyword = st.text_input("🔍 검색", placeholder="키워드 입력...")
    
    st.markdown("---")
    
    # 탭 구성
    tab1, tab2 = st.tabs(["📋 대화 목록", "📊 통계"])
    
    with tab1:
        if st.session_state.selected_conversation_id:
            # 상세보기
            show_conversation_detail(st.session_state.selected_conversation_id)
        elif search_keyword:
            # 검색 결과
            st.markdown(f"### 🔍 '{search_keyword}' 검색 결과")
            results = HistoryManager.search_conversations(
                st.session_state.history_user_id,
                search_keyword
            )
            
            if results:
                for conv in results:
                    date_str = conv['start_time'].strftime('%Y년 %m월 %d일 %H:%M')
                    
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown(f"""
                                <div class="conversation-card">
                                    <h4>🗓️ {date_str}</h4>
                                    <p>
                                        <span class="tag">⏱️ {format_duration(conv['duration'])}</span>
                                        <span class="tag">💬 {conv['message_count']}개 메시지</span>
                                    </p>
                                    {f'<p><small>주제: {conv["main_topics"]}</small></p>' if conv.get('main_topics') else ''}
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if st.button("상세보기", key=f"search_{conv['id']}", use_container_width=True):
                                st.session_state.selected_conversation_id = conv['id']
                                st.rerun()
            else:
                st.info("검색 결과가 없습니다.")
        else:
            # 일반 목록
            show_conversation_list(st.session_state.history_user_id, st.session_state.date_filter)
    
    with tab2:
        show_statistics_dashboard(st.session_state.history_user_id)
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 📋 대화 기록")
        st.markdown("---")

        st.info("""
            **💡 기록 활용 팁**
            
            - 과거 대화를 다시 보며 추억을 떠올려보세요
            - 자주 언급되는 주제를 파악할 수 있습니다
            - 대화를 내보내서 가족과 공유하세요
        """)


if __name__ == "__main__":
    main()
