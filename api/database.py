from typing import Optional

import mysql.connector
from mysql.connector import Error

from api.config import DB_CONFIG


def get_user_profile(user_id: int) -> Optional[dict]:
    """대상자 정보를 RAG 컨텍스트용으로 조회합니다."""
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                name, gender, birth_year, past_job, residence,
                favorite_food, memorable_place, favorite_song, important_people
            FROM users
            WHERE id = %s
            """,
            (user_id,),
        )
        return cursor.fetchone()
    except Error:
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def format_user_context(user: dict) -> str:
    """대상자 정보를 프롬프트용 텍스트로 변환합니다."""
    lines = [f"대상자 이름: {user.get('name', '미상')}"]

    field_labels = {
        "gender": "성별",
        "birth_year": "출생연도",
        "past_job": "과거 직업",
        "residence": "거주 지역",
        "favorite_food": "좋아하던 음식",
        "memorable_place": "추억의 장소",
        "favorite_song": "좋아했던 노래/가수",
        "important_people": "주변 중요 인물",
    }

    for field, label in field_labels.items():
        value = user.get(field)
        if value:
            lines.append(f"{label}: {value}")

    return "\n".join(lines)
