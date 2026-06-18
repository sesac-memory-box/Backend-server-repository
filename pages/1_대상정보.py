"""
대상 정보 입력 페이지
대상자(어르신) 정보 등록 및 관리
"""

import streamlit as st
from datetime import datetime
from typing import Optional
import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_user import UserManager

# 전국 시군구 데이터
KOREA_REGIONS = {
    "서울특별시": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    "부산광역시": ["강서구", "금정구", "남구", "동래구", "동구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
    "대구광역시": ["남구", "달서구", "동구", "북구", "서구", "수성구", "중구"],
    "인천광역시": ["강화군", "계양구", "남동구", "동구", "미추홀구", "부평구", "서구", "연수구", "옹진군", "중구"],
    "광주광역시": ["광산구", "남구", "동구", "북구", "서구"],
    "대전광역시": ["대덕구", "동구", "서구", "유성구", "중구"],
    "울산광역시": ["남구", "동구", "북구", "울주군", "중구"],
    "세종특별자치시": ["세종특별자치시"],
    "경기도": ["가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"],
    "강원특별자치도": ["강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군", "원주시", "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군", "횡성군"],
    "충청북도": ["괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "제천시", "증평군", "진천군", "청주시", "충주시"],
    "충청남도": ["계룡시", "공주시", "금산군", "논산시", "당진시", "보령시", "부여군", "서산시", "서천군", "아산시", "예산군", "천안시", "청양군", "태안군", "홍성군"],
    "전북특별자치도": ["고창군", "군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "임실군", "장수군", "전주시", "정읍시", "진안군"],
    "전라남도": ["강진군", "고흥군", "곡성군", "광양시", "구례군", "나주시", "담양군", "목포시", "무안군", "보성군", "순천시", "신안군", "여수시", "영광군", "영암군", "완도군", "장성군", "장흥군", "진도군", "함평군", "해남군", "화순군"],
    "경상북도": ["경산시", "경주시", "고령군", "구미시", "군위군", "김천시", "문경시", "봉화군", "상주시", "성주군", "안동시", "영덕군", "영양군", "영주시", "영천시", "예천군", "울진군", "울릉군", "의성군", "청도군", "청송군", "칠곡군", "포항시"],
    "경상남도": ["거제시", "거창군", "고성군", "김해시", "남해군", "밀양시", "사천시", "산청군", "양산시", "의령군", "창녕군", "창원시", "통영시", "하동군", "함안군", "함양군", "합천군"],
    "제주특별자치도": ["서귀포시", "제주시"]
}

# 페이지 설정
st.set_page_config(
    page_title="대상 정보 입력 - 기억상자 AI",
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
        background-color: #D2B48C;
        color: #333 !important;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
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

    /* 폼 제출 버튼 */
    button[kind="formSubmit"] {
        background-color: #D2B48C !important;
        color: #333 !important;
    }

    button[kind="formSubmit"]:hover {
        background-color: #C4A574 !important;
    }

    /* 모든 버튼 강제 적용 */
    button {
        background-color: #D2B48C !important;
        color: #333 !important;
    }

    button:hover {
        background-color: #C4A574 !important;
    }
    
    /* 텍스트 색상 */
    .stMarkdown, p, span, div, label {
        color: #333 !important;
    }
    
    /* 섹션 타이틀 가운데 정렬 */
    .section-title {
        text-align: center !important;
        margin: 1.5rem 0 1rem 0 !important;
        border: none !important;
        border-left: none !important;
    }

    /* 입력 필드 폭 조정 및 가운데 정렬 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        border: 2px solid #E8DCC4;
        border-radius: 10px;
        padding: 0.8rem;
        background-color: white !important;
        color: #333 !important;
        max-width: 600px !important;
        margin: 0 auto !important;
    }

    /* 컨테이너 테두리 제거 */
    .stTextInput>div, .stTextArea>div, .stSelectbox>div,
    .stTextInput>div>div, .stTextArea>div>div, .stSelectbox>div>div {
        border: none !important;
    }

    /* 컨테이너 가운데 정렬 */
    .stTextInput>div, .stTextArea>div, .stSelectbox>div {
        display: flex;
        justify-content: center;
    }

    /* 라벨 가운데 정렬 */
    .stTextInput label, .stSelectbox label {
        text-align: center !important;
        display: block;
        margin: 0 auto !important;
    }

    /* 검은 자국 제거 - 모든 컨테이너 */
    .stTextInput>div, .stTextArea>div, .stSelectbox>div,
    .stTextInput>div>div, .stTextArea>div>div, .stSelectbox>div>div {
        background-color: transparent !important;
    }

    /* 전체 배경색 설정 */
    .stApp {
        background-color: #FFF8DC !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #D2691E;
        box-shadow: 0 0 0 3px rgba(210, 105, 30, 0.1);
    }
    
    /* 셀렉트박스 드롭다운 */
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
        border: 2px solid #E8DCC4 !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div:hover {
        border-color: #D2691E !important;
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
    
    .stSelectbox>div>div>div[data-baseweb="select"] {
        background-color: white !important;
    }
    
    .stSelectbox [role="listbox"] {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stSelectbox [role="option"] {
        color: #333 !important;
        background-color: white !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: #F5F5DC !important;
    }
    
    .stSelectbox [role="option"][aria-selected="true"] {
        background-color: #F5F5DC !important;
        color: #333 !important;
    }
    
    /* 전역 셀렉트박스 */
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
    
    [data-baseweb="menu"] li {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background-color: #F5F5DC;
    }
    
    /* 드롭다운 메뉴 추가 스타일 */
    div[data-baseweb="popover"] > div {
        background-color: white !important;
        color: #333 !important;
    }
    
    div[data-baseweb="popover"] > div > div {
        background-color: white !important;
        color: #333 !important;
    }
    
    div[data-baseweb="popover"] ul {
        background-color: white !important;
        color: #333 !important;
    }
    
    div[data-baseweb="popover"] li {
        background-color: white !important;
        color: #333 !important;
    }
    
    div[data-baseweb="popover"] li div {
        background-color: white !important;
        color: #333 !important;
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
                st.caption(f"{user['gender'] or '-'}")
            
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
    
    st.markdown("#### 주의사항 (민감한 주제)")
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
        st.markdown('<div class="section-title">👤 기본 정보</div>', unsafe_allow_html=True)
        name = st.text_input(
            "이름",
            value=user['name'] if user else "",
            placeholder="예: 김영희",
            help="대상자의 이름을 입력해주세요"
        )
        
        gender = st.selectbox(
            "성별",
            options=["선택안함", "남성", "여성", "기타"],
            index=["선택안함", "남성", "여성", "기타"].index(user['gender']) if user and user['gender'] else 0
        )
        
        # 과거 직업
        st.markdown('<div class="section-title">💼 과거 직업</div>', unsafe_allow_html=True)
        past_job = st.text_area(
            "과거 직업",
            value=user['past_job'] if user else "",
            placeholder="예: 초등학교 교사, 농사, 간호사",
            help="과거에 하셨던 일이나 직업을 입력해주세요",
            label_visibility="collapsed"
        )
        
        # 거주 지역
        st.markdown('<div class="section-title">🏘️ 거주 지역</div>', unsafe_allow_html=True)
        
        # 기존 값에서 시/도 추출
        residence_province = "서울특별시"
        
        if user and user['residence'] and isinstance(user['residence'], str) and user['residence'].strip():
            # 기존 값 파싱 (예: "서울특별시 강남구" 또는 "서울 강남구")
            parts = user['residence'].split()
            if len(parts) >= 1:
                for province in KOREA_REGIONS.keys():
                    if province in parts[0]:
                        residence_province = province
                        break
        
        residence = st.selectbox(
            "시/도",
            options=list(KOREA_REGIONS.keys()),
            index=list(KOREA_REGIONS.keys()).index(residence_province) if residence_province in KOREA_REGIONS else 0,
            key="residence_province"
        )
        
        # 좋아하는 음식
        st.markdown('<div class="section-title">🍲 좋아하는 음식</div>', unsafe_allow_html=True)
        favorite_food = st.text_area(
            "좋아하는 음식",
            value=user['favorite_food'] if user else "",
            placeholder="예: 된장찌개, 김치전, 막걸리",
            label_visibility="collapsed"
        )
        
        # 추억의 장소
        st.markdown('<div class="section-title">📍 추억의 장소</div>', unsafe_allow_html=True)
        
        # 기존 값에서 시/도 추출
        memorable_province = "서울특별시"
        
        if user and user['memorable_place'] and isinstance(user['memorable_place'], str) and user['memorable_place'].strip():
            # 기존 값 파싱
            parts = user['memorable_place'].split()
            if len(parts) >= 1:
                for province in KOREA_REGIONS.keys():
                    if province in parts[0]:
                        memorable_province = province
                        break
        
        memorable_place = st.selectbox(
            "시/도",
            options=list(KOREA_REGIONS.keys()),
            index=list(KOREA_REGIONS.keys()).index(memorable_province) if memorable_province in KOREA_REGIONS else 0,
            key="memorable_province"
        )
        
        # 좋아했던 노래/가수
        st.markdown('<div class="section-title">🎵 좋아했던 노래 / 가수</div>', unsafe_allow_html=True)
        favorite_song = st.text_area(
            "좋아했던 노래/가수",
            value=user['favorite_song'] if user else "",
            placeholder="예: 이미자 - 동백아가씨, 패티김",
            label_visibility="collapsed"
        )
        
        # 주의사항
        st.markdown('<div class="section-title">⚠️ 주의사항 (민감한 주제)</div>', unsafe_allow_html=True)
        important_people = st.text_area(
            "주의사항",
            value=user['important_people'] if user else "",
            placeholder="예: 병명, 가족 문제 등 대화 시 피해야 할 민감한 주제",
            help="대화 시 피해야 할 민감한 주제를 입력해주세요",
            label_visibility="collapsed"
        )
        
        # 제출 버튼
        submitted = st.form_submit_button(
            "✅ 저장하기" if not user else "✅ 수정사항 저장하기",
            use_container_width=True
        )
        
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
            <h1>👤 대상 정보 입력</h1>
            <p>대화를 함께할 어르신의 정보를 입력해 주세요</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 대상자 등록/수정
    if st.session_state.selected_user_id and st.session_state.edit_mode:
        # 수정 모드
        show_user_form(st.session_state.selected_user_id)
    elif st.session_state.selected_user_id and not st.session_state.edit_mode:
        # 상세보기 모드
        show_user_detail(st.session_state.selected_user_id)
    else:
        # 신규 등록 모드
        show_user_form()
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 👤 대상 정보 관리")
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
