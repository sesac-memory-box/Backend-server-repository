"""
모듈 4: 대화내역/요약 Read 모듈
대화 내역 조회 및 요약 정보 관리 기능 제공
"""

from typing import Optional, List, Dict
from datetime import datetime, timedelta
from .db_config import execute_query, fetch_one_dict, fetch_all_dict


class HistoryManager:
    """대화 내역 및 요약 관리 클래스"""
    
    @staticmethod
    def get_user_conversations(
        user_id: int, 
        limit: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        대상자의 대화 내역 목록 조회
        
        Args:
            user_id: 대상자 ID
            limit: 조회할 최대 개수 (None이면 전체)
            status: 상태 필터 ('진행중', '완료', None)
            
        Returns:
            List[Dict]: 대화 내역 리스트 (최신순)
        """
        try:
            if status:
                if limit:
                    query = """
                        SELECT 
                            c.id, c.session_id, c.start_time, c.end_time,
                            c.duration, c.message_count, c.status,
                            u.name as user_name
                        FROM conversations c
                        JOIN users u ON c.user_id = u.id
                        WHERE c.user_id = %s AND c.status = %s
                        ORDER BY c.start_time DESC
                        LIMIT %s
                    """
                    params = (user_id, status, limit)
                else:
                    query = """
                        SELECT 
                            c.id, c.session_id, c.start_time, c.end_time,
                            c.duration, c.message_count, c.status,
                            u.name as user_name
                        FROM conversations c
                        JOIN users u ON c.user_id = u.id
                        WHERE c.user_id = %s AND c.status = %s
                        ORDER BY c.start_time DESC
                    """
                    params = (user_id, status)
            else:
                if limit:
                    query = """
                        SELECT 
                            c.id, c.session_id, c.start_time, c.end_time,
                            c.duration, c.message_count, c.status,
                            u.name as user_name
                        FROM conversations c
                        JOIN users u ON c.user_id = u.id
                        WHERE c.user_id = %s
                        ORDER BY c.start_time DESC
                        LIMIT %s
                    """
                    params = (user_id, limit)
                else:
                    query = """
                        SELECT 
                            c.id, c.session_id, c.start_time, c.end_time,
                            c.duration, c.message_count, c.status,
                            u.name as user_name
                        FROM conversations c
                        JOIN users u ON c.user_id = u.id
                        WHERE c.user_id = %s
                        ORDER BY c.start_time DESC
                    """
                    params = (user_id,)
            
            results = fetch_all_dict(query, params)
            return results
            
        except Exception as e:
            print(f"[ERROR] 대화 내역 조회 오류: {e}")
            return []
    
    
    @staticmethod
    def get_conversations_by_date(
        user_id: int,
        date: datetime
    ) -> List[Dict]:
        """
        특정 날짜의 대화 내역 조회
        
        Args:
            user_id: 대상자 ID
            date: 조회할 날짜
            
        Returns:
            List[Dict]: 해당 날짜의 대화 내역 리스트
        """
        try:
            query = """
                SELECT 
                    c.id, c.session_id, c.start_time, c.end_time,
                    c.duration, c.message_count, c.status,
                    u.name as user_name
                FROM conversations c
                JOIN users u ON c.user_id = u.id
                WHERE c.user_id = %s 
                  AND DATE(c.start_time) = DATE(%s)
                ORDER BY c.start_time ASC
            """
            
            results = fetch_all_dict(query, (user_id, date))
            return results
            
        except Exception as e:
            print(f"[ERROR] 날짜별 대화 조회 오류: {e}")
            return []
    
    
    @staticmethod
    def get_conversations_by_date_range(
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        기간별 대화 내역 조회
        
        Args:
            user_id: 대상자 ID
            start_date: 시작 날짜
            end_date: 종료 날짜
            
        Returns:
            List[Dict]: 기간 내 대화 내역 리스트
        """
        try:
            query = """
                SELECT 
                    c.id, c.session_id, c.start_time, c.end_time,
                    c.duration, c.message_count, c.status,
                    u.name as user_name
                FROM conversations c
                JOIN users u ON c.user_id = u.id
                WHERE c.user_id = %s 
                  AND DATE(c.start_time) BETWEEN DATE(%s) AND DATE(%s)
                ORDER BY c.start_time DESC
            """
            
            results = fetch_all_dict(query, (user_id, start_date, end_date))
            return results
            
        except Exception as e:
            print(f"[ERROR] 기간별 대화 조회 오류: {e}")
            return []
    
    
    @staticmethod
    def get_today_conversations(user_id: int) -> List[Dict]:
        """
        오늘의 대화 내역 조회
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            List[Dict]: 오늘의 대화 내역 리스트
        """
        today = datetime.now()
        return HistoryManager.get_conversations_by_date(user_id, today)
    
    
    @staticmethod
    def get_conversation_detail(conversation_id: int) -> Optional[Dict]:
        """
        대화 상세 정보 조회 (메시지 포함)
        
        Args:
            conversation_id: 대화 세션 ID
            
        Returns:
            Dict: 대화 정보 및 메시지 리스트
        """
        try:
            # 대화 기본 정보 조회
            conv_query = """
                SELECT 
                    c.id, c.session_id, c.start_time, c.end_time,
                    c.duration, c.message_count, c.status,
                    u.id as user_id, u.name as user_name, u.birth_year
                FROM conversations c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = %s
            """
            
            conversation = fetch_one_dict(conv_query, (conversation_id,))
            
            if not conversation:
                return None
            
            # 메시지 조회
            msg_query = """
                SELECT 
                    id, speaker, content, audio_file, timestamp
                FROM messages
                WHERE conversation_id = %s
                ORDER BY timestamp ASC
            """
            
            messages = fetch_all_dict(msg_query, (conversation_id,))
            
            # 결합
            conversation['messages'] = messages
            
            return conversation
            
        except Exception as e:
            print(f"[ERROR] 대화 상세 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def create_summary(
        conversation_id: int,
        ai_summary: Optional[str] = None,
        mentioned_people: Optional[str] = None,
        main_topics: Optional[str] = None,
        emotional_tone: Optional[str] = None,
        suggested_questions: Optional[str] = None
    ) -> Optional[int]:
        """
        대화 요약 생성
        
        Args:
            conversation_id: 대화 세션 ID
            ai_summary: AI가 생성한 대화 요약
            mentioned_people: 언급된 인물
            main_topics: 주요 주제/키워드
            emotional_tone: 감정 반응
            suggested_questions: 다음 대화 제안 질문
            
        Returns:
            int: 요약 ID (실패 시 None)
        """
        try:
            query = """
                INSERT INTO summaries (
                    conversation_id, ai_summary, mentioned_people,
                    main_topics, emotional_tone, suggested_questions
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            params = (
                conversation_id, ai_summary, mentioned_people,
                main_topics, emotional_tone, suggested_questions
            )
            
            summary_id = execute_query(query, params, commit=True)
            
            if summary_id:
                print(f"[OK] 대화 요약 생성 완료 (ID: {summary_id})")
                return summary_id
            
            return None
            
        except Exception as e:
            print(f"[ERROR] 대화 요약 생성 오류: {e}")
            return None
    
    
    @staticmethod
    def get_summary(conversation_id: int) -> Optional[Dict]:
        """
        대화 요약 조회
        
        Args:
            conversation_id: 대화 세션 ID
            
        Returns:
            Dict: 요약 정보
        """
        try:
            query = """
                SELECT 
                    id, conversation_id, ai_summary, mentioned_people,
                    main_topics, emotional_tone, suggested_questions,
                    created_at
                FROM summaries
                WHERE conversation_id = %s
            """
            
            result = fetch_one_dict(query, (conversation_id,))
            return result
            
        except Exception as e:
            print(f"[ERROR] 대화 요약 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def update_summary(
        conversation_id: int,
        ai_summary: Optional[str] = None,
        mentioned_people: Optional[str] = None,
        main_topics: Optional[str] = None,
        emotional_tone: Optional[str] = None,
        suggested_questions: Optional[str] = None
    ) -> bool:
        """
        대화 요약 수정
        
        Args:
            conversation_id: 대화 세션 ID
            ai_summary~suggested_questions: 수정할 필드들
            
        Returns:
            bool: 성공 여부
        """
        try:
            # 업데이트할 필드와 값 수집
            update_fields = []
            params = []
            
            if ai_summary is not None:
                update_fields.append("ai_summary = %s")
                params.append(ai_summary)
            
            if mentioned_people is not None:
                update_fields.append("mentioned_people = %s")
                params.append(mentioned_people)
            
            if main_topics is not None:
                update_fields.append("main_topics = %s")
                params.append(main_topics)
            
            if emotional_tone is not None:
                update_fields.append("emotional_tone = %s")
                params.append(emotional_tone)
            
            if suggested_questions is not None:
                update_fields.append("suggested_questions = %s")
                params.append(suggested_questions)
            
            if not update_fields:
                print("[WARN] 업데이트할 필드가 없습니다.")
                return False
            
            query = f"""
                UPDATE summaries 
                SET {', '.join(update_fields)}
                WHERE conversation_id = %s
            """
            params.append(conversation_id)
            
            affected_rows = execute_query(query, tuple(params), commit=True)
            
            if affected_rows > 0:
                print(f"[OK] 대화 요약 업데이트 완료 (conversation_id: {conversation_id})")
                return True
            else:
                print("[WARN] 대화 요약을 찾을 수 없습니다.")
                return False
                
        except Exception as e:
            print(f"[ERROR] 대화 요약 수정 오류: {e}")
            return False
    
    
    @staticmethod
    def get_user_statistics(user_id: int) -> Optional[Dict]:
        """
        대상자의 대화 통계 조회
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            Dict: 통계 정보 (총 대화 수, 총 메시지 수, 평균 대화 시간 등)
        """
        try:
            query = """
                SELECT 
                    COUNT(*) as total_conversations,
                    SUM(message_count) as total_messages,
                    AVG(duration) as avg_duration,
                    SUM(duration) as total_duration,
                    MAX(start_time) as last_conversation_date,
                    COUNT(CASE WHEN status = '완료' THEN 1 END) as completed_conversations
                FROM conversations
                WHERE user_id = %s
            """
            
            result = fetch_one_dict(query, (user_id,))
            return result
            
        except Exception as e:
            print(f"[ERROR] 대화 통계 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def get_recent_topics(user_id: int, limit: int = 10) -> List[str]:
        """
        최근 대화 주제 조회
        
        Args:
            user_id: 대상자 ID
            limit: 조회할 최대 개수
            
        Returns:
            List[str]: 주제 리스트
        """
        try:
            query = """
                SELECT s.main_topics
                FROM summaries s
                JOIN conversations c ON s.conversation_id = c.id
                WHERE c.user_id = %s AND s.main_topics IS NOT NULL
                ORDER BY s.created_at DESC
                LIMIT %s
            """
            
            results = fetch_all_dict(query, (user_id, limit))
            topics = [r['main_topics'] for r in results if r['main_topics']]
            
            return topics
            
        except Exception as e:
            print(f"[ERROR] 최근 주제 조회 오류: {e}")
            return []
    
    
    @staticmethod
    def search_conversations(
        user_id: int,
        keyword: str
    ) -> List[Dict]:
        """
        대화 내용 검색 (메시지 내용, 요약, 주제에서 검색)
        
        Args:
            user_id: 대상자 ID
            keyword: 검색 키워드
            
        Returns:
            List[Dict]: 검색 결과 리스트
        """
        try:
            query = """
                SELECT DISTINCT
                    c.id, c.session_id, c.start_time, c.end_time,
                    c.duration, c.message_count, c.status,
                    s.main_topics, s.ai_summary
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                LEFT JOIN summaries s ON c.id = s.conversation_id
                WHERE c.user_id = %s 
                  AND (
                    m.content LIKE %s 
                    OR s.ai_summary LIKE %s
                    OR s.main_topics LIKE %s
                    OR s.mentioned_people LIKE %s
                  )
                ORDER BY c.start_time DESC
            """
            
            search_pattern = f"%{keyword}%"
            params = (user_id, search_pattern, search_pattern, search_pattern, search_pattern)
            
            results = fetch_all_dict(query, params)
            return results
            
        except Exception as e:
            print(f"[ERROR] 대화 검색 오류: {e}")
            return []
    
    
    @staticmethod
    def get_monthly_conversation_count(user_id: int, year: int, month: int) -> int:
        """
        월별 대화 횟수 조회
        
        Args:
            user_id: 대상자 ID
            year: 연도
            month: 월
            
        Returns:
            int: 대화 횟수
        """
        try:
            query = """
                SELECT COUNT(*) as count
                FROM conversations
                WHERE user_id = %s 
                  AND YEAR(start_time) = %s 
                  AND MONTH(start_time) = %s
            """
            
            result = fetch_one_dict(query, (user_id, year, month))
            return result['count'] if result else 0
            
        except Exception as e:
            print(f"[ERROR] 월별 대화 횟수 조회 오류: {e}")
            return 0


# 편의 함수들
def get_user_conversations(user_id: int, limit: Optional[int] = None) -> List[Dict]:
    """대화 내역 조회 편의 함수"""
    return HistoryManager.get_user_conversations(user_id, limit)


def get_conversation_detail(conversation_id: int) -> Optional[Dict]:
    """대화 상세 조회 편의 함수"""
    return HistoryManager.get_conversation_detail(conversation_id)


def create_summary(conversation_id: int, **kwargs) -> Optional[int]:
    """요약 생성 편의 함수"""
    return HistoryManager.create_summary(conversation_id, **kwargs)


def get_summary(conversation_id: int) -> Optional[Dict]:
    """요약 조회 편의 함수"""
    return HistoryManager.get_summary(conversation_id)


def get_user_statistics(user_id: int) -> Optional[Dict]:
    """통계 조회 편의 함수"""
    return HistoryManager.get_user_statistics(user_id)


if __name__ == "__main__":
    # 모듈 테스트
    print("=" * 50)
    print("대화내역/요약 Read 테스트")
    print("=" * 50)
    
    # 테스트용 대상자 ID (실제로는 존재하는 ID 사용)
    test_user_id = 1
    
    # 1. 대화 내역 조회
    print("\n1. 대화 내역 조회 테스트")
    conversations = get_user_conversations(test_user_id, limit=5)
    print(f"대화 내역: {len(conversations)}건")
    
    # 2. 통계 조회
    print("\n2. 대화 통계 테스트")
    stats = get_user_statistics(test_user_id)
    if stats:
        print(f"총 대화 수: {stats['total_conversations']}")
        print(f"총 메시지 수: {stats['total_messages']}")
        print(f"평균 대화 시간: {stats['avg_duration']}초")
    
    # 3. 오늘의 대화
    print("\n3. 오늘의 대화 조회 테스트")
    today_convs = HistoryManager.get_today_conversations(test_user_id)
    print(f"오늘의 대화: {len(today_convs)}건")
    
    print("\n" + "=" * 50)
    print("테스트 완료")
    print("=" * 50)
