"""
모듈 2: 대상정보 CRUD 모듈
대상자(어르신) 정보의 생성, 조회, 수정, 삭제 기능 제공
"""

from typing import Optional, List, Dict, Tuple
from datetime import datetime
from .db_config import execute_query, fetch_one_dict, fetch_all_dict, get_db_connection


class UserManager:
    """대상자 정보 관리 클래스"""
    
    @staticmethod
    def create_user(
        name: str,
        gender: Optional[str] = None,
        birth_year: Optional[int] = None,
        past_job: Optional[str] = None,
        residence: Optional[str] = None,
        favorite_food: Optional[str] = None,
        memorable_place: Optional[str] = None,
        favorite_song: Optional[str] = None,
        important_people: Optional[str] = None,
        profile_image: Optional[str] = None
    ) -> Optional[int]:
        """
        새로운 대상자 등록
        
        Args:
            name: 이름 (필수)
            gender: 성별 ('남성', '여성', '기타')
            birth_year: 출생연도
            past_job: 과거 직업
            residence: 거주했던 지역
            favorite_food: 좋아하던 음식
            memorable_place: 추억의 장소
            favorite_song: 좋아했던 노래/가수
            important_people: 주변 중요 인물
            profile_image: 프로필 이미지 경로
            
        Returns:
            int: 생성된 사용자 ID (실패 시 None)
        """
        try:
            query = """
                INSERT INTO users (
                    name, gender, birth_year, past_job, residence,
                    favorite_food, memorable_place, favorite_song, 
                    important_people, profile_image
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                name, gender, birth_year, past_job, residence,
                favorite_food, memorable_place, favorite_song,
                important_people, profile_image
            )
            
            user_id = execute_query(query, params, commit=True)
            print(f"✅ 대상자 '{name}' 등록 완료 (ID: {user_id})")
            return user_id
            
        except Exception as e:
            print(f"❌ 대상자 등록 오류: {e}")
            return None
    
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        """
        ID로 대상자 정보 조회
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            Dict: 대상자 정보 딕셔너리 (없으면 None)
        """
        try:
            query = """
                SELECT 
                    id, name, gender, birth_year, past_job, residence,
                    favorite_food, memorable_place, favorite_song,
                    important_people, profile_image, created_at, updated_at
                FROM users
                WHERE id = %s
            """
            
            result = fetch_one_dict(query, (user_id,))
            return result
            
        except Exception as e:
            print(f"❌ 대상자 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def get_user_by_name(name: str) -> Optional[Dict]:
        """
        이름으로 대상자 정보 조회 (첫 번째 매치)
        
        Args:
            name: 대상자 이름
            
        Returns:
            Dict: 대상자 정보 딕셔너리 (없으면 None)
        """
        try:
            query = """
                SELECT 
                    id, name, gender, birth_year, past_job, residence,
                    favorite_food, memorable_place, favorite_song,
                    important_people, profile_image, created_at, updated_at
                FROM users
                WHERE name = %s
                LIMIT 1
            """
            
            result = fetch_one_dict(query, (name,))
            return result
            
        except Exception as e:
            print(f"❌ 대상자 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def get_all_users() -> List[Dict]:
        """
        모든 대상자 목록 조회 (최신순)
        
        Returns:
            List[Dict]: 대상자 정보 리스트
        """
        try:
            query = """
                SELECT 
                    id, name, gender, birth_year, past_job, residence,
                    favorite_food, memorable_place, favorite_song,
                    important_people, profile_image, created_at, updated_at
                FROM users
                ORDER BY created_at DESC
            """
            
            results = fetch_all_dict(query)
            return results
            
        except Exception as e:
            print(f"❌ 대상자 목록 조회 오류: {e}")
            return []
    
    
    @staticmethod
    def get_users_summary() -> List[Dict]:
        """
        대상자 요약 목록 조회 (ID, 이름, 성별, 생년만)
        
        Returns:
            List[Dict]: 대상자 요약 정보 리스트
        """
        try:
            query = """
                SELECT 
                    id, name, gender, birth_year, created_at
                FROM users
                ORDER BY created_at DESC
            """
            
            results = fetch_all_dict(query)
            return results
            
        except Exception as e:
            print(f"❌ 대상자 요약 조회 오류: {e}")
            return []
    
    
    @staticmethod
    def update_user(
        user_id: int,
        name: Optional[str] = None,
        gender: Optional[str] = None,
        birth_year: Optional[int] = None,
        past_job: Optional[str] = None,
        residence: Optional[str] = None,
        favorite_food: Optional[str] = None,
        memorable_place: Optional[str] = None,
        favorite_song: Optional[str] = None,
        important_people: Optional[str] = None,
        profile_image: Optional[str] = None
    ) -> bool:
        """
        대상자 정보 수정 (제공된 필드만 업데이트)
        
        Args:
            user_id: 대상자 ID
            name~profile_image: 수정할 필드들 (None이 아닌 값만 업데이트)
            
        Returns:
            bool: 성공 여부
        """
        try:
            # 업데이트할 필드와 값 수집
            update_fields = []
            params = []
            
            if name is not None:
                update_fields.append("name = %s")
                params.append(name)
            
            if gender is not None:
                update_fields.append("gender = %s")
                params.append(gender)
            
            if birth_year is not None:
                update_fields.append("birth_year = %s")
                params.append(birth_year)
            
            if past_job is not None:
                update_fields.append("past_job = %s")
                params.append(past_job)
            
            if residence is not None:
                update_fields.append("residence = %s")
                params.append(residence)
            
            if favorite_food is not None:
                update_fields.append("favorite_food = %s")
                params.append(favorite_food)
            
            if memorable_place is not None:
                update_fields.append("memorable_place = %s")
                params.append(memorable_place)
            
            if favorite_song is not None:
                update_fields.append("favorite_song = %s")
                params.append(favorite_song)
            
            if important_people is not None:
                update_fields.append("important_people = %s")
                params.append(important_people)
            
            if profile_image is not None:
                update_fields.append("profile_image = %s")
                params.append(profile_image)
            
            # 업데이트할 필드가 없으면 종료
            if not update_fields:
                print("⚠️ 업데이트할 필드가 없습니다.")
                return False
            
            # 쿼리 생성
            query = f"""
                UPDATE users 
                SET {', '.join(update_fields)}
                WHERE id = %s
            """
            params.append(user_id)
            
            affected_rows = execute_query(query, tuple(params), commit=True)
            
            if affected_rows > 0:
                print(f"✅ 대상자 ID {user_id} 정보 업데이트 완료")
                return True
            else:
                print(f"⚠️ 대상자 ID {user_id}를 찾을 수 없습니다.")
                return False
                
        except Exception as e:
            print(f"❌ 대상자 정보 수정 오류: {e}")
            return False
    
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        대상자 삭제 (연관된 대화 기록도 함께 삭제됨 - CASCADE)
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            query = "DELETE FROM users WHERE id = %s"
            
            affected_rows = execute_query(query, (user_id,), commit=True)
            
            if affected_rows > 0:
                print(f"✅ 대상자 ID {user_id} 삭제 완료")
                return True
            else:
                print(f"⚠️ 대상자 ID {user_id}를 찾을 수 없습니다.")
                return False
                
        except Exception as e:
            print(f"❌ 대상자 삭제 오류: {e}")
            return False
    
    
    @staticmethod
    def user_exists(user_id: int) -> bool:
        """
        대상자 존재 여부 확인
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            bool: 존재 여부
        """
        try:
            query = "SELECT COUNT(*) as count FROM users WHERE id = %s"
            result = fetch_one_dict(query, (user_id,))
            
            return result['count'] > 0 if result else False
            
        except Exception as e:
            print(f"❌ 대상자 존재 확인 오류: {e}")
            return False
    
    
    @staticmethod
    def get_user_age(user_id: int) -> Optional[int]:
        """
        대상자 나이 계산
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            int: 나이 (출생연도가 없으면 None)
        """
        try:
            user = UserManager.get_user_by_id(user_id)
            
            if user and user.get('birth_year'):
                current_year = datetime.now().year
                age = current_year - user['birth_year']
                return age
            
            return None
            
        except Exception as e:
            print(f"❌ 나이 계산 오류: {e}")
            return None
    
    
    @staticmethod
    def get_user_decade(user_id: int) -> Optional[str]:
        """
        대상자가 살았던 주요 시대 구간 계산
        (청년기 20-30대를 기준으로 어느 연대를 살았는지)
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            str: 연대 (예: "1960s", "1970s") 또는 None
        """
        try:
            user = UserManager.get_user_by_id(user_id)
            
            if user and user.get('birth_year'):
                # 25세 때의 연도를 기준으로 연대 계산
                youth_year = user['birth_year'] + 25
                decade = (youth_year // 10) * 10
                return f"{decade}s"
            
            return None
            
        except Exception as e:
            print(f"❌ 연대 계산 오류: {e}")
            return None
    
    
    @staticmethod
    def search_users(keyword: str) -> List[Dict]:
        """
        대상자 검색 (이름, 과거 직업, 거주지역에서 검색)
        
        Args:
            keyword: 검색 키워드
            
        Returns:
            List[Dict]: 검색 결과 리스트
        """
        try:
            query = """
                SELECT 
                    id, name, gender, birth_year, past_job, residence,
                    created_at
                FROM users
                WHERE name LIKE %s 
                   OR past_job LIKE %s 
                   OR residence LIKE %s
                ORDER BY created_at DESC
            """
            
            search_pattern = f"%{keyword}%"
            params = (search_pattern, search_pattern, search_pattern)
            
            results = fetch_all_dict(query, params)
            return results
            
        except Exception as e:
            print(f"❌ 대상자 검색 오류: {e}")
            return []


# 편의 함수들
def create_user(**kwargs) -> Optional[int]:
    """대상자 생성 편의 함수"""
    return UserManager.create_user(**kwargs)


def get_user(user_id: int) -> Optional[Dict]:
    """대상자 조회 편의 함수"""
    return UserManager.get_user_by_id(user_id)


def get_all_users() -> List[Dict]:
    """전체 대상자 목록 조회 편의 함수"""
    return UserManager.get_all_users()


def update_user(user_id: int, **kwargs) -> bool:
    """대상자 정보 수정 편의 함수"""
    return UserManager.update_user(user_id, **kwargs)


def delete_user(user_id: int) -> bool:
    """대상자 삭제 편의 함수"""
    return UserManager.delete_user(user_id)


if __name__ == "__main__":
    # 모듈 테스트
    print("=" * 50)
    print("대상자 정보 CRUD 테스트")
    print("=" * 50)
    
    # 1. 대상자 생성
    print("\n1. 대상자 생성 테스트")
    user_id = create_user(
        name="테스트 할머니",
        gender="여성",
        birth_year=1950,
        past_job="간호사",
        residence="부산 해운대",
        favorite_food="밀면, 돼지국밥",
        memorable_place="광안리 해수욕장",
        favorite_song="패티김 - 사랑의 미로",
        important_people="남편: 김철수, 딸: 김영희, 아들: 김민수"
    )
    
    if user_id:
        # 2. 대상자 조회
        print("\n2. 대상자 조회 테스트")
        user = get_user(user_id)
        if user:
            print(f"이름: {user['name']}")
            print(f"나이: {UserManager.get_user_age(user_id)}세")
            print(f"연대: {UserManager.get_user_decade(user_id)}")
        
        # 3. 대상자 수정
        print("\n3. 대상자 정보 수정 테스트")
        update_user(user_id, past_job="간호사 (부산대학교병원)")
        
        # 4. 대상자 검색
        print("\n4. 대상자 검색 테스트")
        results = UserManager.search_users("부산")
        print(f"검색 결과: {len(results)}건")
        
        # 5. 대상자 삭제
        print("\n5. 대상자 삭제 테스트")
        delete_user(user_id)
    
    print("\n" + "=" * 50)
    print("테스트 완료")
    print("=" * 50)
