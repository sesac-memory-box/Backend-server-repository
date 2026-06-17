"""
모듈 1: MySQL 공통 연동 설정 모듈
데이터베이스 연결 풀 관리 및 공통 쿼리 실행 함수 제공
"""

import mysql.connector
from mysql.connector import pooling, Error
import os
from dotenv import load_dotenv
import streamlit as st
from typing import Optional, List, Tuple, Any, Dict
from contextlib import contextmanager

# 환경변수 로드
load_dotenv()

# 데이터베이스 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'memory_box'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False
}

# 연결 풀 설정
CONNECTION_POOL_CONFIG = {
    'pool_name': 'memory_box_pool',
    'pool_size': 5,
    'pool_reset_session': True
}

# 전역 연결 풀 변수
_connection_pool: Optional[pooling.MySQLConnectionPool] = None


def init_connection_pool():
    """
    데이터베이스 연결 풀 초기화
    Streamlit 세션에서 한 번만 실행되도록 캐싱
    """
    global _connection_pool
    
    if _connection_pool is None:
        try:
            _connection_pool = pooling.MySQLConnectionPool(
                **DB_CONFIG,
                **CONNECTION_POOL_CONFIG
            )
            print("✅ 데이터베이스 연결 풀 초기화 완료")
        except Error as e:
            print(f"❌ 연결 풀 초기화 오류: {e}")
            st.error(f"데이터베이스 연결 실패: {e}")
            raise
    
    return _connection_pool


def get_connection():
    """
    연결 풀에서 데이터베이스 연결 가져오기
    
    Returns:
        mysql.connector.connection.MySQLConnection: 데이터베이스 연결 객체
        
    Raises:
        Error: 연결 실패 시
    """
    try:
        if _connection_pool is None:
            init_connection_pool()
        
        connection = _connection_pool.get_connection()
        
        if connection.is_connected():
            return connection
        else:
            raise Error("연결이 활성화되지 않았습니다.")
            
    except Error as e:
        print(f"❌ 데이터베이스 연결 오류: {e}")
        st.error(f"데이터베이스 연결 오류: {e}")
        raise


def close_connection(connection):
    """
    데이터베이스 연결 종료 (풀로 반환)
    
    Args:
        connection: MySQL 연결 객체
    """
    try:
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"⚠️ 연결 종료 오류: {e}")


@contextmanager
def get_db_connection():
    """
    Context Manager로 안전한 데이터베이스 연결 관리
    
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 쿼리 실행
    """
    connection = None
    try:
        connection = get_connection()
        yield connection
    except Error as e:
        if connection:
            connection.rollback()
        print(f"❌ 데이터베이스 오류: {e}")
        raise
    finally:
        if connection:
            close_connection(connection)


def execute_query(
    query: str, 
    params: Optional[Tuple] = None, 
    commit: bool = True
) -> Optional[int]:
    """
    INSERT, UPDATE, DELETE 쿼리 실행
    
    Args:
        query: 실행할 SQL 쿼리
        params: 쿼리 파라미터 (튜플)
        commit: 자동 커밋 여부
        
    Returns:
        int: 영향받은 행 수 또는 마지막 삽입 ID (INSERT의 경우)
        
    Raises:
        Error: 쿼리 실행 실패 시
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(query, params or ())
        
        if commit:
            connection.commit()
        
        # INSERT 쿼리의 경우 마지막 삽입 ID 반환
        if query.strip().upper().startswith('INSERT'):
            return cursor.lastrowid
        else:
            return cursor.rowcount
            
    except Error as e:
        if connection:
            connection.rollback()
        print(f"❌ 쿼리 실행 오류: {e}")
        print(f"쿼리: {query}")
        print(f"파라미터: {params}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)


def fetch_one(query: str, params: Optional[Tuple] = None) -> Optional[Tuple]:
    """
    단일 행 조회 쿼리 실행
    
    Args:
        query: 실행할 SELECT 쿼리
        params: 쿼리 파라미터 (튜플)
        
    Returns:
        Tuple: 조회된 행 (없으면 None)
        
    Raises:
        Error: 쿼리 실행 실패 시
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        
        return result
        
    except Error as e:
        print(f"❌ 쿼리 실행 오류: {e}")
        print(f"쿼리: {query}")
        print(f"파라미터: {params}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)


def fetch_all(query: str, params: Optional[Tuple] = None) -> List[Tuple]:
    """
    다중 행 조회 쿼리 실행
    
    Args:
        query: 실행할 SELECT 쿼리
        params: 쿼리 파라미터 (튜플)
        
    Returns:
        List[Tuple]: 조회된 모든 행 (빈 리스트 가능)
        
    Raises:
        Error: 쿼리 실행 실패 시
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        
        return results
        
    except Error as e:
        print(f"❌ 쿼리 실행 오류: {e}")
        print(f"쿼리: {query}")
        print(f"파라미터: {params}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)


def fetch_one_dict(query: str, params: Optional[Tuple] = None) -> Optional[Dict]:
    """
    단일 행을 딕셔너리로 조회
    
    Args:
        query: 실행할 SELECT 쿼리
        params: 쿼리 파라미터 (튜플)
        
    Returns:
        Dict: 조회된 행을 딕셔너리로 변환 (없으면 None)
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        
        return result
        
    except Error as e:
        print(f"❌ 쿼리 실행 오류: {e}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)


def fetch_all_dict(query: str, params: Optional[Tuple] = None) -> List[Dict]:
    """
    다중 행을 딕셔너리 리스트로 조회
    
    Args:
        query: 실행할 SELECT 쿼리
        params: 쿼리 파라미터 (튜플)
        
    Returns:
        List[Dict]: 조회된 모든 행을 딕셔너리 리스트로 변환
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        
        return results
        
    except Error as e:
        print(f"❌ 쿼리 실행 오류: {e}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_connection(connection)


def test_connection() -> bool:
    """
    데이터베이스 연결 테스트
    
    Returns:
        bool: 연결 성공 여부
    """
    try:
        connection = get_connection()
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ MySQL 서버 연결 성공 (버전: {db_info})")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"✅ 현재 데이터베이스: {db_name}")
            
            cursor.close()
            close_connection(connection)
            return True
        else:
            print("❌ 데이터베이스 연결 실패")
            return False
            
    except Error as e:
        print(f"❌ 연결 테스트 오류: {e}")
        return False


# Streamlit 앱 시작 시 연결 풀 초기화
if 'db_pool_initialized' not in st.session_state:
    try:
        init_connection_pool()
        st.session_state.db_pool_initialized = True
    except Exception as e:
        st.error(f"⚠️ 데이터베이스 초기화 실패: {e}")
        st.info("💡 .env 파일의 데이터베이스 설정을 확인하고 MySQL 서버가 실행 중인지 확인하세요.")


if __name__ == "__main__":
    # 모듈 테스트
    print("=" * 50)
    print("데이터베이스 연결 테스트")
    print("=" * 50)
    test_connection()
