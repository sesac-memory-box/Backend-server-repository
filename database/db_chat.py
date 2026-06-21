"""
모듈 3: 대화내용 Create/Read 모듈
대화 세션 생성 및 메시지 저장/조회 기능 제공
"""

from typing import Optional, List, Dict, Tuple
from datetime import datetime
import uuid
from .db_config import execute_query, fetch_one_dict, fetch_all_dict, get_db_connection


class ChatManager:
    """대화 관리 클래스"""
    
    @staticmethod
    def create_conversation(user_id: int) -> Optional[Tuple[int, str]]:
        """
        새로운 대화 세션 생성
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            Tuple[int, str]: (conversation_id, session_id) 또는 None
        """
        try:
            # 고유한 세션 ID 생성
            session_id = f"session_{uuid.uuid4().hex[:16]}_{int(datetime.now().timestamp())}"
            
            query = """
                INSERT INTO conversations (user_id, session_id, status)
                VALUES (%s, %s, '진행중')
            """
            
            conversation_id = execute_query(query, (user_id, session_id), commit=True)
            
            if conversation_id:
                print(f"[OK] 대화 세션 생성 완료 (ID: {conversation_id}, Session: {session_id})")
                return (conversation_id, session_id)
            
            return None
            
        except Exception as e:
            print(f"[ERROR] 대화 세션 생성 오류: {e}")
            return None
    
    
    @staticmethod
    def get_conversation_by_id(conversation_id: int) -> Optional[Dict]:
        """
        대화 세션 정보 조회
        
        Args:
            conversation_id: 대화 세션 ID
            
        Returns:
            Dict: 대화 세션 정보
        """
        try:
            query = """
                SELECT 
                    id, user_id, session_id, start_time, end_time,
                    duration, message_count, status, created_at
                FROM conversations
                WHERE id = %s
            """
            
            result = fetch_one_dict(query, (conversation_id,))
            return result
            
        except Exception as e:
            print(f"[ERROR] 대화 세션 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def get_conversation_by_session_id(session_id: str) -> Optional[Dict]:
        """
        세션 ID로 대화 세션 정보 조회
        
        Args:
            session_id: 세션 고유 ID
            
        Returns:
            Dict: 대화 세션 정보
        """
        try:
            query = """
                SELECT 
                    id, user_id, session_id, start_time, end_time,
                    duration, message_count, status, created_at
                FROM conversations
                WHERE session_id = %s
            """
            
            result = fetch_one_dict(query, (session_id,))
            return result
            
        except Exception as e:
            print(f"[ERROR] 대화 세션 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def get_active_conversation(user_id: int) -> Optional[Dict]:
        """
        진행 중인 대화 세션 조회
        
        Args:
            user_id: 대상자 ID
            
        Returns:
            Dict: 진행 중인 대화 세션 정보 (없으면 None)
        """
        try:
            query = """
                SELECT 
                    id, user_id, session_id, start_time, end_time,
                    duration, message_count, status, created_at
                FROM conversations
                WHERE user_id = %s AND status = '진행중'
                ORDER BY start_time DESC
                LIMIT 1
            """
            
            result = fetch_one_dict(query, (user_id,))
            return result
            
        except Exception as e:
            print(f"[ERROR] 진행 중 대화 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def add_message(
        conversation_id: int,
        speaker: str,
        content: str,
        audio_file: Optional[str] = None
    ) -> Optional[int]:
        """
        대화 메시지 추가
        
        Args:
            conversation_id: 대화 세션 ID
            speaker: 발화자 ('user' 또는 'ai')
            content: 메시지 내용
            audio_file: 음성 파일 경로 (선택)
            
        Returns:
            int: 메시지 ID (실패 시 None)
        """
        try:
            # 메시지 삽입
            query = """
                INSERT INTO messages (conversation_id, speaker, content, audio_file)
                VALUES (%s, %s, %s, %s)
            """
            
            message_id = execute_query(
                query, 
                (conversation_id, speaker, content, audio_file),
                commit=True
            )
            
            if message_id:
                # 대화 세션의 메시지 카운트 업데이트
                update_query = """
                    UPDATE conversations 
                    SET message_count = message_count + 1
                    WHERE id = %s
                """
                execute_query(update_query, (conversation_id,), commit=True)
                
                print(f"[OK] 메시지 추가 완료 (ID: {message_id})")
                return message_id
            
            return None
            
        except Exception as e:
            print(f"[ERROR] 메시지 추가 오류: {e}")
            return None
    
    
    @staticmethod
    def get_messages(conversation_id: int, limit: Optional[int] = None) -> List[Dict]:
        """
        대화 세션의 메시지 목록 조회
        
        Args:
            conversation_id: 대화 세션 ID
            limit: 조회할 최대 메시지 수 (None이면 전체)
            
        Returns:
            List[Dict]: 메시지 리스트 (시간순)
        """
        try:
            if limit:
                query = """
                    SELECT 
                        id, conversation_id, speaker, content, 
                        audio_file, timestamp
                    FROM messages
                    WHERE conversation_id = %s
                    ORDER BY timestamp ASC
                    LIMIT %s
                """
                params = (conversation_id, limit)
            else:
                query = """
                    SELECT 
                        id, conversation_id, speaker, content, 
                        audio_file, timestamp
                    FROM messages
                    WHERE conversation_id = %s
                    ORDER BY timestamp ASC
                """
                params = (conversation_id,)
            
            results = fetch_all_dict(query, params)
            return results
            
        except Exception as e:
            print(f"[ERROR] 메시지 조회 오류: {e}")
            return []
    
    
    @staticmethod
    def get_recent_messages(conversation_id: int, count: int = 10) -> List[Dict]:
        """
        최근 메시지 N개 조회
        
        Args:
            conversation_id: 대화 세션 ID
            count: 조회할 메시지 개수
            
        Returns:
            List[Dict]: 최근 메시지 리스트 (시간순)
        """
        try:
            query = """
                SELECT 
                    id, conversation_id, speaker, content, 
                    audio_file, timestamp
                FROM messages
                WHERE conversation_id = %s
                ORDER BY timestamp DESC
                LIMIT %s
            """
            
            results = fetch_all_dict(query, (conversation_id, count))
            # 시간순으로 정렬 (오름차순)
            results.reverse()
            return results
            
        except Exception as e:
            print(f"[ERROR] 최근 메시지 조회 오류: {e}")
            return []
    
    
    @staticmethod
    def end_conversation(conversation_id: int) -> bool:
        """
        대화 세션 종료
        
        Args:
            conversation_id: 대화 세션 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            # 대화 시간 계산
            query = """
                UPDATE conversations
                SET 
                    status = '완료',
                    end_time = CURRENT_TIMESTAMP,
                    duration = TIMESTAMPDIFF(SECOND, start_time, CURRENT_TIMESTAMP)
                WHERE id = %s AND status = '진행중'
            """
            
            affected_rows = execute_query(query, (conversation_id,), commit=True)
            
            if affected_rows > 0:
                print(f"[OK] 대화 세션 {conversation_id} 종료 완료")
                return True
            else:
                print(f"[WARN] 대화 세션 {conversation_id}를 찾을 수 없거나 이미 종료되었습니다.")
                return False
                
        except Exception as e:
            print(f"[ERROR] 대화 세션 종료 오류: {e}")
            return False
    
    
    @staticmethod
    def get_message_count(conversation_id: int) -> int:
        """
        대화 세션의 메시지 개수 조회
        
        Args:
            conversation_id: 대화 세션 ID
            
        Returns:
            int: 메시지 개수
        """
        try:
            query = """
                SELECT COUNT(*) as count 
                FROM messages 
                WHERE conversation_id = %s
            """
            
            result = fetch_one_dict(query, (conversation_id,))
            return result['count'] if result else 0
            
        except Exception as e:
            print(f"[ERROR] 메시지 개수 조회 오류: {e}")
            return 0
    
    
    @staticmethod
    def get_conversation_duration(conversation_id: int) -> Optional[int]:
        """
        대화 세션의 지속 시간 조회 (초)
        
        Args:
            conversation_id: 대화 세션 ID
            
        Returns:
            int: 대화 지속 시간 (초) 또는 None
        """
        try:
            conversation = ChatManager.get_conversation_by_id(conversation_id)
            
            if conversation:
                if conversation['status'] == '완료' and conversation['duration']:
                    return conversation['duration']
                elif conversation['status'] == '진행중':
                    # 진행 중이면 현재까지의 시간 계산
                    query = """
                        SELECT TIMESTAMPDIFF(SECOND, start_time, CURRENT_TIMESTAMP) as duration
                        FROM conversations
                        WHERE id = %s
                    """
                    result = fetch_one_dict(query, (conversation_id,))
                    return result['duration'] if result else 0
            
            return None
            
        except Exception as e:
            print(f"[ERROR] 대화 시간 조회 오류: {e}")
            return None
    
    
    @staticmethod
    def delete_conversation(conversation_id: int) -> bool:
        """
        대화 세션 삭제 (메시지도 함께 삭제됨 - CASCADE)
        
        Args:
            conversation_id: 대화 세션 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            query = "DELETE FROM conversations WHERE id = %s"
            
            affected_rows = execute_query(query, (conversation_id,), commit=True)
            
            if affected_rows > 0:
                print(f"[OK] 대화 세션 {conversation_id} 삭제 완료")
                return True
            else:
                print(f"[WARN] 대화 세션 {conversation_id}를 찾을 수 없습니다.")
                return False
                
        except Exception as e:
            print(f"[ERROR] 대화 세션 삭제 오류: {e}")
            return False
    
    
    @staticmethod
    def get_conversation_summary(conversation_id: int) -> Optional[Dict]:
        """
        대화 세션 요약 정보 조회
        
        Args:
            conversation_id: 대화 세션 ID
            
        Returns:
            Dict: 요약 정보 (대화 시간, 메시지 수, 사용자/AI 메시지 비율 등)
        """
        try:
            query = """
                SELECT 
                    c.id,
                    c.session_id,
                    c.start_time,
                    c.end_time,
                    c.duration,
                    c.message_count,
                    c.status,
                    COUNT(CASE WHEN m.speaker = 'user' THEN 1 END) as user_messages,
                    COUNT(CASE WHEN m.speaker = 'ai' THEN 1 END) as ai_messages,
                    u.name as user_name
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                LEFT JOIN users u ON c.user_id = u.id
                WHERE c.id = %s
                GROUP BY c.id
            """
            
            result = fetch_one_dict(query, (conversation_id,))
            return result
            
        except Exception as e:
            print(f"[ERROR] 대화 요약 조회 오류: {e}")
            return None


# 편의 함수들
def create_conversation(user_id: int) -> Optional[Tuple[int, str]]:
    """대화 세션 생성 편의 함수"""
    return ChatManager.create_conversation(user_id)


def add_message(conversation_id: int, speaker: str, content: str, audio_file: Optional[str] = None) -> Optional[int]:
    """메시지 추가 편의 함수"""
    return ChatManager.add_message(conversation_id, speaker, content, audio_file)


def get_messages(conversation_id: int, limit: Optional[int] = None) -> List[Dict]:
    """메시지 조회 편의 함수"""
    return ChatManager.get_messages(conversation_id, limit)


def end_conversation(conversation_id: int) -> bool:
    """대화 종료 편의 함수"""
    return ChatManager.end_conversation(conversation_id)


if __name__ == "__main__":
    # 모듈 테스트
    print("=" * 50)
    print("대화내용 Create/Read 테스트")
    print("=" * 50)
    
    # 테스트용 대상자 ID (실제로는 존재하는 ID 사용)
    test_user_id = 1
    
    # 1. 대화 세션 생성
    print("\n1. 대화 세션 생성 테스트")
    result = create_conversation(test_user_id)
    
    if result:
        conversation_id, session_id = result
        print(f"대화 세션 ID: {conversation_id}")
        print(f"세션 ID: {session_id}")
        
        # 2. 메시지 추가
        print("\n2. 메시지 추가 테스트")
        add_message(conversation_id, 'ai', '안녕하세요! 오늘은 어떤 추억을 이야기할까요?')
        add_message(conversation_id, 'user', '옛날에 살던 고향 이야기를 하고 싶어요.')
        add_message(conversation_id, 'ai', '고향은 어디셨나요? 그때 어떤 풍경이 기억나시나요?')
        
        # 3. 메시지 조회
        print("\n3. 메시지 조회 테스트")
        messages = get_messages(conversation_id)
        print(f"총 메시지 수: {len(messages)}")
        for msg in messages:
            print(f"[{msg['speaker']}] {msg['content']}")
        
        # 4. 대화 요약
        print("\n4. 대화 요약 테스트")
        summary = ChatManager.get_conversation_summary(conversation_id)
        if summary:
            print(f"사용자 메시지: {summary['user_messages']}개")
            print(f"AI 메시지: {summary['ai_messages']}개")
            print(f"상태: {summary['status']}")
        
        # 5. 대화 종료
        print("\n5. 대화 종료 테스트")
        end_conversation(conversation_id)
        
        # 6. 대화 삭제
        print("\n6. 대화 삭제 테스트")
        ChatManager.delete_conversation(conversation_id)
    
    print("\n" + "=" * 50)
    print("테스트 완료")
    print("=" * 50)
