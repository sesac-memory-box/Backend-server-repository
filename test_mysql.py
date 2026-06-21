"""
MySQL 연결 테스트 스크립트
"""
import mysql.connector
from dotenv import load_dotenv
import os

# 환경변수 로드
load_dotenv()

print("=" * 50)
print("MySQL 연결 테스트")
print("=" * 50)

# 설정 출력
print(f"\n📋 연결 정보:")
print(f"  Host: {os.getenv('DB_HOST')}")
print(f"  Port: {os.getenv('DB_PORT')}")
print(f"  User: {os.getenv('DB_USER')}")
print(f"  Password: {'*' * len(os.getenv('DB_PASSWORD', ''))}")
print(f"  Database: {os.getenv('DB_NAME')}")

try:
    print("\n🔄 연결 시도 중...")
    
    # 데이터베이스 없이 연결 시도
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )
    
    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"\n✅ MySQL 서버 연결 성공!")
        print(f"   버전: {db_info}")
        
        # 데이터베이스 목록 조회
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        print(f"\n📂 사용 가능한 데이터베이스:")
        for db in databases:
            print(f"   - {db[0]}")
        
        # memory_box 데이터베이스 확인
        db_name = os.getenv('DB_NAME', 'memory_box')
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()
        
        if result:
            print(f"\n✅ '{db_name}' 데이터베이스가 이미 존재합니다.")
        else:
            print(f"\n⚠️  '{db_name}' 데이터베이스가 없습니다. init_db.py를 실행하세요.")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 50)
        print("✅ 연결 테스트 성공!")
        print("=" * 50)
        
except mysql.connector.Error as e:
    print(f"\n❌ 연결 실패!")
    print(f"   오류 코드: {e.errno}")
    print(f"   오류 메시지: {e.msg}")
    
    if e.errno == 1045:
        print("\n💡 해결 방법:")
        print("   - .env 파일의 DB_PASSWORD를 확인하세요")
        print("   - MySQL 사용자 이름(DB_USER)을 확인하세요")
    elif e.errno == 2003:
        print("\n💡 해결 방법:")
        print("   - MySQL 서비스가 실행 중인지 확인하세요")
        print("   - 방화벽 설정을 확인하세요")
    
    print("\n" + "=" * 50)
    
except Exception as e:
    print(f"\n❌ 예상치 못한 오류: {e}")
    print("=" * 50)
