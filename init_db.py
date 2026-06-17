"""
기억상자 AI - 데이터베이스 초기화 스크립트
MySQL 데이터베이스와 테이블을 생성합니다.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def create_database():
    """데이터베이스 생성"""
    try:
        # 데이터베이스 없이 MySQL 연결
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            db_name = os.getenv('DB_NAME', 'memory_box')
            
            # 데이터베이스 생성
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ 데이터베이스 '{db_name}' 생성 완료")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ 데이터베이스 생성 오류: {e}")
        return False

def create_tables():
    """테이블 생성"""
    try:
        # 데이터베이스 연결
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'memory_box')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 1. 대상정보 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL COMMENT '이름',
                    gender ENUM('남성', '여성', '기타') COMMENT '성별',
                    birth_year INT COMMENT '출생연도',
                    past_job TEXT COMMENT '과거 직업',
                    residence TEXT COMMENT '거주했던 지역',
                    favorite_food TEXT COMMENT '좋아하던 음식',
                    memorable_place TEXT COMMENT '추억의 장소',
                    favorite_song TEXT COMMENT '좋아했던 노래/가수',
                    important_people TEXT COMMENT '주변 중요 인물 (관계명, 이름)',
                    profile_image VARCHAR(255) COMMENT '프로필 이미지 경로',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_name (name),
                    INDEX idx_created (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='대상자 정보';
            """)
            print("✅ 'users' 테이블 생성 완료")
            
            # 2. 대화세션 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL COMMENT '대상자 ID',
                    session_id VARCHAR(100) UNIQUE NOT NULL COMMENT '세션 고유 ID',
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '시작 시간',
                    end_time TIMESTAMP NULL COMMENT '종료 시간',
                    duration INT COMMENT '대화 시간(초)',
                    message_count INT DEFAULT 0 COMMENT '메시지 개수',
                    status ENUM('진행중', '완료') DEFAULT '진행중',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user (user_id),
                    INDEX idx_session (session_id),
                    INDEX idx_start_time (start_time)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='대화 세션';
            """)
            print("✅ 'conversations' 테이블 생성 완료")
            
            # 3. 대화메시지 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    conversation_id INT NOT NULL COMMENT '대화 세션 ID',
                    speaker ENUM('user', 'ai') NOT NULL COMMENT '발화자',
                    content TEXT NOT NULL COMMENT '메시지 내용',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '메시지 시간',
                    audio_file VARCHAR(255) COMMENT '음성 파일 경로',
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
                    INDEX idx_conversation (conversation_id),
                    INDEX idx_timestamp (timestamp)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='대화 메시지';
            """)
            print("✅ 'messages' 테이블 생성 완료")
            
            # 4. 대화요약 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    conversation_id INT NOT NULL COMMENT '대화 세션 ID',
                    ai_summary TEXT COMMENT 'AI가 생성한 대화 요약',
                    mentioned_people TEXT COMMENT '언급된 인물',
                    main_topics TEXT COMMENT '주요 주제/키워드',
                    emotional_tone VARCHAR(100) COMMENT '감정 반응',
                    suggested_questions TEXT COMMENT '다음 대화 제안 질문',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
                    INDEX idx_conversation (conversation_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='대화 요약';
            """)
            print("✅ 'summaries' 테이블 생성 완료")
            
            # 5. 회상 소재 테이블 (선택적)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory_contents (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    category VARCHAR(50) COMMENT '카테고리 (영화, 음악, 역사, 생활문화 등)',
                    decade VARCHAR(10) COMMENT '연대 (1950s, 1960s 등)',
                    title VARCHAR(255) COMMENT '제목',
                    description TEXT COMMENT '설명',
                    image_url VARCHAR(255) COMMENT '이미지 URL',
                    source VARCHAR(100) COMMENT '출처',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_category (category),
                    INDEX idx_decade (decade)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='회상 대화 소재';
            """)
            print("✅ 'memory_contents' 테이블 생성 완료")
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ 테이블 생성 오류: {e}")
        return False

def insert_sample_data():
    """샘플 데이터 삽입 (선택적)"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'memory_box')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 샘플 대상자 추가 확인
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                cursor.execute("""
                    INSERT INTO users (name, gender, birth_year, past_job, residence, 
                                      favorite_food, memorable_place, favorite_song, important_people)
                    VALUES 
                    ('김영희', '여성', 1945, '교사', '서울 종로구', 
                     '된장찌개, 김치전', '남산, 명동 거리', '이미자 - 동백아가씨', 
                     '남편: 김철수, 딸: 김민지')
                """)
                print("✅ 샘플 대상자 데이터 추가 완료")
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ 샘플 데이터 삽입 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("🏠 기억상자 AI - 데이터베이스 초기화")
    print("=" * 50)
    
    # .env 파일 확인
    if not os.path.exists('.env'):
        print("\n⚠️  .env 파일이 없습니다!")
        print("📝 .env.example을 복사하여 .env 파일을 만들고 설정값을 입력하세요.")
        return
    
    print("\n1️⃣  데이터베이스 생성 중...")
    if not create_database():
        print("\n❌ 데이터베이스 생성 실패")
        return
    
    print("\n2️⃣  테이블 생성 중...")
    if not create_tables():
        print("\n❌ 테이블 생성 실패")
        return
    
    print("\n3️⃣  샘플 데이터 추가 중...")
    insert_sample_data()
    
    print("\n" + "=" * 50)
    print("✅ 데이터베이스 초기화 완료!")
    print("=" * 50)
    print("\n💡 이제 'streamlit run app.py' 명령으로 서비스를 시작할 수 있습니다.")

if __name__ == "__main__":
    main()
