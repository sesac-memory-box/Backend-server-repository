# 🏠 기억상자 AI

치매 어르신을 위한 회상 대화 서비스

## 📋 프로젝트 소개

기억상자 AI는 치매 어르신들이 편안하게 과거를 떠올리고 말할 수 있는 AI 기반 대화 서비스입니다.
새로운 정보를 학습하는 것보다 익숙한 과거 경험을 바탕으로 대화할 때 더 자연스럽게 소통할 수 있습니다.

### 주요 기능
- 🎤 음성 인식 기반 대화
- 💬 감각과 경험 중심의 회상 질문
- 📊 대화 내역 및 요약 관리
- 👤 대상자 정보 관리 (과거 직업, 추억의 장소, 좋아하던 노래 등)

## 🚀 설치 방법

### 1. 필수 요구사항
- Python 3.9 이상
- MySQL 8.0 이상

### 2. 프로젝트 설치

```bash
# 저장소 클론 (또는 압축 해제)
cd "Memory Box"

# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env.example` 파일을 `.env`로 복사하고 실제 값을 입력하세요:

```bash
copy .env.example .env
```

`.env` 파일 수정:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=실제_비밀번호
DB_NAME=memory_box

OPENAI_API_KEY=실제_OpenAI_API_키
```

### 4. 데이터베이스 초기화

```bash
python init_db.py
```

## 💻 실행 방법

```bash
streamlit run app.py
```

브라우저에서 자동으로 `http://localhost:8501` 열립니다.

## 📁 프로젝트 구조

```
Memory Box/
├── app.py                  # 메인 페이지
├── pages/                  # Streamlit 페이지들
│   ├── 1_대상정보.py
│   ├── 2_AI대화.py
│   ├── 3_이전대화기록.py
│   └── 4_오늘대화요약.py
├── database/              # 데이터베이스 모듈
│   ├── db_config.py      # MySQL 공통 설정
│   ├── db_user.py        # 대상정보 CRUD
│   ├── db_chat.py        # 대화내용 저장/조회
│   └── db_history.py     # 대화내역/요약 조회
├── init_db.py            # DB 초기화 스크립트
├── requirements.txt      # 패키지 목록
├── .env                  # 환경변수 (git 제외)
└── README.md            # 프로젝트 문서
```

## 🗄️ 데이터베이스 스키마

### users (대상정보)
- 이름, 성별, 생년월일
- 과거 직업, 거주지역
- 좋아하던 음식, 추억의 장소
- 좋아했던 노래/가수
- 주변 중요 인물

### conversations (대화세션)
- 대화 세션 ID
- 대상자 ID
- 시작/종료 시간

### messages (대화메시지)
- 대화 세션 ID
- 발화자 (사용자/AI)
- 메시지 내용
- 타임스탬프

### summaries (대화요약)
- 대화 세션 ID
- 주요 주제, 언급된 인물
- 감정 반응
- 제안 질문

## 📊 데이터 소스

1. **노인 음성 데이터** (AI Hub) - STT 성능 검증
2. **근현대 생활문화 데이터** (대한민국역사박물관) - 회상 대화 소재
3. **영화 데이터** (KMDb API) - 영화·배우 회상

## 🔒 개인정보 보호

- 모든 대상자 정보는 로컬 MySQL에만 저장
- 민감정보는 암호화 권장
- AI API 전송 시 개인식별정보 최소화

## 📝 라이선스

교육용 프로젝트

## 👥 기여

문의사항이나 개선 제안은 이슈로 등록해주세요.
