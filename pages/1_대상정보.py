import streamlit as st
from datetime import datetime

st.set_page_config(page_title="대상 정보 입력 - 기억상자 AI", layout="wide")

# 시/도 데이터
KOREA_REGIONS = ["서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시", "경기도", "강원특별자치도", "충청북도", "충청남도", "전북특별자치도", "전라남도", "경상북도", "경상남도", "제주특별자치도"]

def init_session_state():
    if 'users' not in st.session_state:
        st.session_state.users = []

def main():
    init_session_state()
    st.title("👤 대상자 상세 정보 등록")

    with st.form("user_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("이름", placeholder="예: 김영희")
            gender = st.selectbox("성별", ["선택안함", "남성", "여성"])
            past_job = st.text_input("과거 직업", placeholder="예: 초등학교 교사")
            residence = st.selectbox("거주 지역", KOREA_REGIONS)
        
        with col2:
            favorite_food = st.text_input("좋아하는 음식", placeholder="예: 된장찌개, 김치전")
            memorable_place = st.selectbox("추억의 장소 (지역)", KOREA_REGIONS)
            favorite_song = st.text_input("좋아했던 노래/가수", placeholder="예: 이미자 - 동백아가씨")
        
        important_people = st.text_area("주의사항 (민감한 주제)", placeholder="예: 건강 문제, 가족사 등 피해야 할 주제")

        submitted = st.form_submit_button("✅ 대상자 등록하기")
        
        if submitted:
            if not name:
                st.error("이름은 필수 입력 항목입니다.")
            else:
                new_id = int(datetime.now().timestamp())
                st.session_state.users.append({
                    "id": new_id,
                    "name": name,
                    "gender": gender,
                    "past_job": past_job,
                    "residence": residence,
                    "favorite_food": favorite_food,
                    "memorable_place": memorable_place,
                    "favorite_song": favorite_song,
                    "important_people": important_people,
                    "created_at": datetime.now()
                })
                st.success(f"✅ '{name}' 어르신 정보가 안전하게 등록되었습니다.")

    st.divider()
    st.write("### 📋 등록된 대상자 목록")
    if not st.session_state.users:
        st.info("등록된 정보가 없습니다.")
    else:
        for u in st.session_state.users:
            with st.expander(f"{u['name']} ({u['gender']})"):
                st.write(f"💼 **직업:** {u['past_job']} | 🏠 **거주:** {u['residence']}")
                st.write(f"🍲 **음식:** {u['favorite_food']} | 🎵 **노래:** {u['favorite_song']}")
                st.write(f"⚠️ **주의:** {u['important_people']}")

if __name__ == "__main__":
    main()