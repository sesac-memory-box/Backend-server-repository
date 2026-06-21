"""
기억상자 AI - 메인 페이지
치매 어르신을 위한 회상 대화 서비스
"""

import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime

# 환경변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="기억상자 AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS - 프로토타입 디자인 반영
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
    
    /* 메인 컨테이너 */
    .main .block-container {
        padding-top: 1rem;
        max-width: 900px;
    }
    
    /* 헤더 */
    .main-header {
        text-align: center;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* 환영 박스 */
    .welcome-box {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5F5DC 100%);
        padding: 2rem 1.5rem;
        border-radius: 25px;
        text-align: center;
        margin: 1rem auto;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.1);
    }
    
    .welcome-title {
        font-size: 2rem;
        color: #333;
        margin-bottom: 0.7rem;
        font-weight: 600;
    }
    
    .welcome-subtitle {
        font-size: 1.35rem;
        color: #8B4513;
        font-weight: bold;
        margin: 0.5rem 0;
        line-height: 1.5;
    }
    
    /* 원형 마이크 버튼 */
    .mic-container {
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .mic-circle {
        width: 150px;
        height: 150px;
        background: linear-gradient(135deg, #D2691E 0%, #A0522D 100%);
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(139, 69, 19, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        animation: pulse 2s infinite;
        gap: 0.5rem;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 8px 25px rgba(139, 69, 19, 0.3);
        }
        50% {
            box-shadow: 0 8px 35px rgba(139, 69, 19, 0.5), 0 0 0 10px rgba(210, 105, 30, 0.1);
        }
        100% {
            box-shadow: 0 8px 25px rgba(139, 69, 19, 0.3);
        }
    }
    
    .mic-circle:hover {
        transform: scale(1.08);
        box-shadow: 0 12px 35px rgba(139, 69, 19, 0.4);
        animation: none;
    }
    
    .mic-circle:active {
        transform: scale(0.95);
    }
    
    .mic-icon {
        font-size: 3.2rem;
        color: white;
        animation: mic-bounce 1.5s ease-in-out infinite;
    }

    .mic-text {
        color: white;
        font-size: 0.9rem;
        font-weight: 600;
        text-align: center;
        line-height: 1.2;
    }
    
    @keyframes mic-bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-5px);
        }
    }
    
    /* 안내 문구 개선 */
    .guide-text {
        text-align: center;
        color: #8B4513;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
        animation: fade-in-up 0.8s ease-out;
    }
    
    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .guide-subtext {
        text-align: center;
        color: #999;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    .stButton>button {
        background-color: #D2B48C;
        color: #333 !important;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #C4A574;
        color: #333 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
    }
    
    /* 텍스트 색상 강제 */
    .stMarkdown, p, span, div {
        color: #333 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #8B4513 !important;
    }
    
    /* 입력 필드 텍스트 */
    input, textarea, select {
        color: #333 !important;
    }
    
    /* 라벨 텍스트 */
    label {
        color: #666 !important;
    }
    
    /* 안내 문구 */
    .guide-text {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin: 1rem 0;
    }
    
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background-color: #F5F5DC;
    }
    
    /* 구분선 */
    hr {
        border: none;
        border-top: 2px solid #E8DCC4;
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """세션 상태 초기화"""
    if 'current_user_id' not in st.session_state:
        st.session_state.current_user_id = None
    
    if 'current_conversation_id' not in st.session_state:
        st.session_state.current_conversation_id = None
    
    if 'recording' not in st.session_state:
        st.session_state.recording = False


def main():
    """메인 페이지"""
    init_session_state()
    
    # 헤더
    st.markdown("""
        <div class="main-header">
            <h1 style="color: #8B4513; font-size: 2rem; margin-bottom: 0.5rem;">🏠 기억상자 AI</h1>
            <p style="color: #666; font-size: 1rem;">추억을 떠나는 여행</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 환영 메시지
    st.markdown("""
        <div class="welcome-box">
            <div class="welcome-title">좋은 오후예요 😊</div>
            <div class="welcome-subtitle">오늘은 어떤<br><span style="color: #D2691E;">추억</span>을<br>이야기할까요?</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 원형 마이크 버튼
    st.markdown("""
        <div class="mic-container">
            <div class="mic-circle">
                <div class="mic-icon">🎤</div>
                <div class="mic-text">버튼을 눌러<br>말씀하세요</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 🏠 기억상자 AI")
        st.markdown("---")
        
        # 데이터베이스 연결 상태
        try:
            from database.db_config import test_connection
            if test_connection():
                st.success("✅ 데이터베이스 연결됨")
            else:
                st.error("❌ 데이터베이스 연결 실패")
        except Exception as e:
            st.error(f"⚠️ 연결 오류: {str(e)}")
        
        st.markdown("---")
        
        # 정보
        st.markdown("### ℹ️ 서비스 정보")
        st.info("""
            **기억상자 AI**는 치매 어르신들이 
            편안하게 과거를 떠올리고 
            대화할 수 있도록 돕는 
            AI 기반 서비스입니다.
        """)
        
        st.markdown("---")
        st.caption(f"© 2026 기억상자 AI")
        st.caption(f"현재 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}")


if __name__ == "__main__":
    main()
