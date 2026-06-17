"""
대상정보 페이지
대상자(어르신) 정보 등록 및 관리
"""

import streamlit as st
from datetime import datetime
import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_user import UserManager

# 페이지 설정
st.set_page_config(
    page_title="대상정보 - 기억상자 AI",
    page_icon="👤",
    layout="wide"
)

# 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background-color: #FFF8DC;
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
    
    .page-header p {
        color: #666;
        font-size: 1.1rem;
    }
    
    /* 폼 섹션 */
    .form-section {
        background-color: #FFF;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 10px rgba(139, 69, 19, 0.08);
    }
    
    /* 섹션 타이틀 */
    .section-title {
        color: #8B4513;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
        padding-left: 0.5rem;
        border-left: 4px solid #D2691E;
    }
    
    /* 안내 박스 */
    .info-box {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5F5DC 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #D2691E;
        margin: 1rem 0;
    }
    
    /* 사용자 카드 */
    .user-card {
        background-color: #FFF;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #E8DCC4;
        transition: all 0.3s ease;
    }
    
    .user-card:hover {
        border-color: #D2691E;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.15);
    }
    
    /* 버튼 */
    .stButton>button {
        background-color: #D2691E;
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-size: 1rem;
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
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        border: 2px solid #E8DCC4;
        border-radius: 10px;
        padding: 0.8rem;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
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
    if 'selected_user_id' not in st.session_state:
        st.session_state.selected_user_id = None
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False


def show_user_list():
    """대상자 목록 표시"""
    st.markdown("### 📋 등록된 대상자 목록")
    
    users = UserManager.get_all_users()
    
    if not users:
        st.info("등록된 대상자가 없습니다. 새로운 대상자를 등록해주세요.")
        return
    
    for user in users:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                st.markdown(f"**{user['name']}**")
                if user['birth_year']:
                    age = datetime.now().year - user['birth_year']
                    st.caption(f"{user['gender']} · {age}세 ({user['birth_year']}년생)")
            
            with col2:
                if user['past_job']:
                    st.caption(f"💼 {user['past_job'][:20]}")
            
            with col3:
                st.caption(f"📅 {user['created_at'].strftime('%Y-%m-%d')}")
            
            with col4:
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button("👁️", key=f"view_{user['id']}", help="상세보기"):
                        st.session_state.selected_user_id = user['id']
                        st.rerun()
                
                with col_btn2:
                    if st.button("✏️", key=f"edit_{user['id']}", help="수정"):
                        st.session_state.selected_user_id = user['id']
                        st.session_state.edit_mode = True
                        st.rerun()
                
                with col_btn3:
                    if st.button("🗑️", key=f"delete_{user['id']}", help="삭제"):
                        if st.session_state.get(f"confirm_delete_{user['id']}", False):
                            UserManager.delete_user(user['id'])
                            st.success(f"'{user['name']}' 대상자가 삭제되었습니다.")
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_{user['id']}"] = True
                            st.warning("한 번 더 클릭하시면 삭제됩니다.")
            
            st.markdown("---")


def show_user_detail(user_id: int):
    """대상자 상세 정보 표시"""
    user = UserManager.get_user_by_id(user_id)
    
    if not user:
        st.error("대상자를 찾을 수 없습니다.")
        return
    
    st.markdown(f"### 👤 {user['name']} 님의 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 기본 정보")
        st.markdown(f"**이름:** {user['name']}")
        st.markdown(f"**성별:** {user['gender'] or '-'}")
        if user['birth_year']:
            age = datetime.now().year - user['birth_year']
            st.markdown(f"**생년월일:** {user['birth_year']}년 ({age}세)")
        
        st.markdown("#### 과거 직업")
        st.info(user['past_job'] or '-')
        
        st.markdown("#### 거주 지역")
        st.info(user['residence'] or '-')
    
    with col2:
        st.markdown("#### 좋아하는 음식")
        st.info(user['favorite_food'] or '-')
        
        st.markdown("#### 추억의 장소")
        st.info(user['memorable_place'] or '-')
        
        st.markdown("#### 좋아했던 노래/가수")
        st.info(user['favorite_song'] or '-')
    
    st.markdown("#### 주변 중요 인물")
    st.info(user['important_people'] or '-')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 목록으로", use_container_width=True):
            st.session_state.selected_user_id = None
            st.rerun()
    
    with col2:
        if st.button("✏️ 수정하기", use_container_width=True, type="primary"):
            st.session_state.edit_mode = True
            st.rerun()


def show_user_form(user_id: Optional[int] = None):
    """대상자 정보 입력/수정 폼"""
    
    # 수정 모드인 경우 기존 정보 불러오기
    user = None
    if user_id:
        user = UserManager.get_user_by_id(user_id)
        st.markdown(f"### ✏️ {user['name']} 님의 정보 수정")
    else:
        st.markdown("### ✨ 새로운 대상자 등록")
    
    # 안내 메시지
    st.markdown("""
        <div class="info-box">
            ℹ️ <strong>입력하신 정보는 AI가 더 자연스럽고 개인화된 대화를 만들어 줍니다.</strong><br>
            💡 <strong>편안한 대화를 위해 가능한 많은 정보를 입력해 주세요.</strong>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("user_form"):
        # 기본 정보
        st.markdown('<div class="section-title">👤 교명</div>', unsafe_allow_html=True)
        name = st.text_input(
            "이름",
            value=user['name'] if user else "",
            placeholder="예: 김영희",
            help="대상자의 이름을 입력해주세요",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">🚻 과거 직업</div>', unsafe_allow_html=True)
            gender = st.selectbox(
                "성별",
                options=["선택안함", "남성", "여성", "기타"],
                index=["선택안함", "남성", "여성", "기타"].index(user['gender']) if user and user['gender'] else 0,
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown('<div class="section-title">🎂 출생연도</div>', unsafe_allow_html=True)
            current_year = datetime.now().year
            birth_year = st.number_input(
                "출생연도",
                min_value=1920,
                max_value=current_year,
                value=user['birth_year'] if user and user['birth_year'] else 1950,
                step=1,
                label_visibility="collapsed"
            )
        
        # 과거 직업
        st.markdown('<div class="section-title">💼 좋아하는 음식</div>', unsafe_allow_html=True)
        past_job = st.text_area(
            "과거 직업",
            value=user['past_job'] if user else "",
            placeholder="예: 초등학교 교사, 농사, 간호사",
            help="과거에 하셨던 일이나 직업을 입력해주세요",
            label_visibility="collapsed"
        )
        
        # 거주 지역
        st.markdown('<div class="section-title">🏘️ 추억의 장소</div>', unsafe_allow_html=True)
        residence = st.text_area(
            "거주 지역",
            value=user['residence'] if user else "",
            placeholder="예: 서울 종로구, 부산 해운대",
            help="살았던 지역을 입력해주세요",
            label_visibility="collapsed"
        )
        
        # 좋아하는 음식
        st.markdown('<div class="section-title">🍲 추억의 장소</div>', unsafe_allow_html=True)
        favorite_food = st.text_area(
            "좋아하는 음식",
            value=user['favorite_food'] if user else "",
            placeholder="예: 된장찌개, 김치전, 막걸리",
            label_visibility="collapsed"
        )
        
        # 추억의 장소
        st.markdown('<div class="section-title">📍 좋아했던 노래 / 가수</div>', unsafe_allow_html=True)
        memorable_place = st.text_area(
            "추억의 장소",
            value=user['memorable_place'] if user else "",
            placeholder="예: 남산 타워, 명동 거리, 고향 앞 개울",
            label_visibility="collapsed"
        )
        
        # 좋아했던 노래/가수
        st.markdown('<div class="section-title">🎵 주변 중요 인물 (선택사항)</div>', unsafe_allow_html=True)
        favorite_song = st.text_area(
            "좋아했던 노래/가수",
            value=user['favorite_song'] if user else "",
            placeholder="예: 이미자 - 동백아가씨, 패티김",
            label_visibility="collapsed"
        )
        
        # 주변 중요 인물
        st.markdown('<div class="section-title">👨‍👩‍👧‍👦 주변 중요 인물 (선택 사항)</div>', unsafe_allow_html=True)
        important_people = st.text_area(
            "주변 중요 인물",
            value=user['important_people'] if user else "",
            placeholder="예: 남편: 김철수, 딸: 김민지, 친구: 이순희",
            help="관계와 이름을 함께 입력해주세요",
            label_visibility="collapsed"
        )
        
        # 제출 버튼
        col1, col2 = st.columns(2)
        
        with col1:
            submitted = st.form_submit_button(
                "✅ 저장하고 등록하기 ✓" if not user else "✅ 수정사항 저장하기",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            cancel = st.form_submit_button(
                "취소",
                use_container_width=True
            )
        
        if cancel:
            st.session_state.selected_user_id = None
            st.session_state.edit_mode = False
            st.rerun()
        
        if submitted:
            # 필수 항목 검증
            if not name:
                st.error("이름은 필수 입력 항목입니다.")
                return
            
            # 성별 처리
            gender_value = None if gender == "선택안함" else gender
            
            try:
                if user:
                    # 수정
                    success = UserManager.update_user(
                        user_id=user['id'],
                        name=name,
                        gender=gender_value,
                        birth_year=birth_year,
                        past_job=past_job if past_job else None,
                        residence=residence if residence else None,
                        favorite_food=favorite_food if favorite_food else None,
                        memorable_place=memorable_place if memorable_place else None,
                        favorite_song=favorite_song if favorite_song else None,
                        important_people=important_people if important_people else None
                    )
                    
                    if success:
                        st.success(f"✅ '{name}' 님의 정보가 수정되었습니다!")
                        st.session_state.edit_mode = False
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("정보 수정에 실패했습니다.")
                else:
                    # 신규 등록
                    new_user_id = UserManager.create_user(
                        name=name,
                        gender=gender_value,
                        birth_year=birth_year,
                        past_job=past_job if past_job else None,
                        residence=residence if residence else None,
                        favorite_food=favorite_food if favorite_food else None,
                        memorable_place=memorable_place if memorable_place else None,
                        favorite_song=favorite_song if favorite_song else None,
                        important_people=important_people if important_people else None
                    )
                    
                    if new_user_id:
                        st.success(f"✅ '{name}' 님이 등록되었습니다!")
                        st.session_state.selected_user_id = new_user_id
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("등록에 실패했습니다.")
            
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")


def main():
    """메인 함수"""
    init_session_state()
    
    # 헤더
    st.markdown("""
        <div class="page-header">
            <h1>👤 보호자 대상 입력</h1>
            <p>대화를 함께할 어르신의 정보를 입력해 주세요</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 탭 구성
    tab1, tab2 = st.tabs(["📝 대상자 등록/수정", "📋 대상자 목록"])
    
    with tab1:
        if st.session_state.selected_user_id and st.session_state.edit_mode:
            # 수정 모드
            show_user_form(st.session_state.selected_user_id)
        elif st.session_state.selected_user_id and not st.session_state.edit_mode:
            # 상세보기 모드
            show_user_detail(st.session_state.selected_user_id)
        else:
            # 신규 등록 모드
            show_user_form()
    
    with tab2:
        show_user_list()
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 👤 대상정보 관리")
        st.markdown("---")
        
        if st.button("🏠 메인으로", use_container_width=True):
            st.switch_page("app.py")
        
        if st.button("💬 AI 대화", use_container_width=True):
            st.switch_page("pages/2_AI대화.py")
        
        st.markdown("---")
        
        st.info("""
            **💡 입력 팁**
            
            - 과거 직업과 거주지는 대화 소재가 됩니다
            - 좋아하던 음식과 장소는 추억을 떠올리는 데 도움이 됩니다
            - 주변 인물 정보는 더 자연스러운 대화를 만듭니다
        """)


if __name__ == "__main__":
    main()
