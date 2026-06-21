"""
더미 데이터 생성 스크립트
현실적인 어르신 정보와 대화 내용을 생성합니다.
"""

import sys
import os
from datetime import datetime, timedelta
import random

# 프로젝트 루트를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_user import UserManager
from database.db_chat import ChatManager
from database.db_history import HistoryManager

# 더미 데이터
DUMMY_USERS = [
    {
        "name": "김영희",
        "gender": "여성",
        "birth_year": 1945,
        "past_job": "초등학교 교사",
        "residence": "서울 종로구, 경기도 수원",
        "favorite_food": "된장찌개, 김치전, 막걸리",
        "memorable_place": "남산 타워, 명동 거리, 창경궁",
        "favorite_song": "이미자 - 동백아가씨, 패티김 - 사랑의 미로",
        "important_people": "남편: 김철수, 딸: 김민지, 아들: 김태희, 친구: 박순자"
    },
    {
        "name": "이순자",
        "gender": "여성",
        "birth_year": 1950,
        "past_job": "간호사 (서울대학교병원)",
        "residence": "부산 해운대, 서울 강남",
        "favorite_food": "밀면, 돼지국밥, 씨앗호떡",
        "memorable_place": "광안리 해수욕장, 자갈치 시장, 태종대",
        "favorite_song": "은방울자매 - 연락선은 떠난다, 나훈아 - 물레방아 도는데",
        "important_people": "남편: 이영호, 딸: 이지은, 아들: 이준호"
    },
    {
        "name": "박철수",
        "gender": "남성",
        "birth_year": 1948,
        "past_job": "농협 직원",
        "residence": "전라북도 전주, 서울 마포",
        "favorite_food": "비빔밥, 콩나물국밥, 막걸리",
        "memorable_place": "한옥마을, 전주 남부시장, 덕진공원",
        "favorite_song": "남진 - 가시나무, 조용필 - 돌아와요 부산항에",
        "important_people": "아내: 최영숙, 딸: 박서연, 아들: 박준영, 친구: 김동수"
    },
    {
        "name": "최영숙",
        "gender": "여성",
        "birth_year": 1952,
        "past_job": "은행원 (국민은행)",
        "residence": "대구 중구, 서울 송파",
        "favorite_food": "막창, 찜갈비, 동인동 찜갈비",
        "memorable_place": "서문시장, 동성로, 팔공산",
        "favorite_song": "심수봉 - 그때 그 사람, 혜은이 - 감수광",
        "important_people": "남편: 박철수, 딸: 박서연, 언니: 최영자"
    },
    {
        "name": "정민호",
        "gender": "남성",
        "birth_year": 1943,
        "past_job": "우체국장",
        "residence": "강원도 춘천, 서울 노원",
        "favorite_food": "닭갈비, 막국수, 감자옹심이",
        "memorable_place": "소양강댐, 남이섬, 춘천 명동",
        "favorite_song": "현인 - 굳세어라 금순아, 백년설 - 봄날은 간다",
        "important_people": "아내: 강순희, 아들: 정우성, 딸: 정미선"
    }
]

# 대화 샘플 (AI와 사용자의 자연스러운 대화)
CONVERSATION_SAMPLES = [
    [
        ("ai", "안녕하세요! 오늘은 어떤 추억을 이야기해볼까요?"),
        ("user", "옛날 서울 명동 거리가 생각나요"),
        ("ai", "명동 거리는 어떤 모습이었나요? 그때 무엇을 하셨어요?"),
        ("user", "젊었을 때 친구들이랑 다방에서 커피 마시고 영화관도 갔지"),
        ("ai", "다방 커피 맛이 어땠나요? 어떤 영화를 보셨나요?"),
        ("user", "그때는 믹스커피도 맛있었어. 명동극장에서 외국 영화 많이 봤어"),
        ("ai", "친구분들과 함께 보낸 시간이 참 즐거우셨겠어요. 특히 기억에 남는 친구가 있으신가요?"),
        ("user", "응, 순자라는 친구가 있었는데 참 재미있는 친구였어")
    ],
    [
        ("ai", "오늘은 어떤 이야기를 나눠볼까요?"),
        ("user", "학교 다닐 때 생각이 나네요"),
        ("ai", "학교에서 어떤 일들이 있었나요? 선생님은 어떠셨어요?"),
        ("user", "우리 담임선생님이 엄하셨는데 지금 생각하면 정말 좋은 선생님이었어"),
        ("ai", "어떤 점이 좋은 선생님이셨나요?"),
        ("user", "공부도 열심히 가르쳐주시고, 가난한 학생들 도와주시고 그랬어"),
        ("ai", "정말 따뜻하신 선생님이셨네요. 그때 학교에서 제일 좋아했던 과목은 뭐였나요?"),
        ("user", "음악 시간이 제일 좋았지. 노래 부르는 거 좋아했거든")
    ],
    [
        ("ai", "좋은 오후예요! 오늘은 어떤 추억을 떠올려볼까요?"),
        ("user", "고향 전주 생각이 나네"),
        ("ai", "전주는 어떤 곳이었나요? 어떤 냄새가 났나요?"),
        ("user", "한옥마을 거리에 콩나물국밥 냄새가 가득했지"),
        ("ai", "맛있는 냄새였겠어요! 전주에서 제일 좋아했던 장소는 어디였나요?"),
        ("user", "남부시장이 제일 좋았어. 거기서 엄마랑 장 보러 많이 갔지"),
        ("ai", "어머니와 함께 시장 가셨던 기억이 있으시군요. 무엇을 사셨나요?"),
        ("user", "과일이랑 채소, 생선도 사고... 엄마가 흥정도 잘 하셨어")
    ],
    [
        ("ai", "안녕하세요! 오늘은 어떤 이야기를 나눠볼까요?"),
        ("user", "요즘 옛날 노래가 자꾸 생각나요"),
        ("ai", "어떤 노래가 생각나시나요? 혹시 함께 부르시던 분이 있으셨나요?"),
        ("user", "이미자의 동백아가씨요. 남편이랑 데이트할 때 자주 들었어요"),
        ("ai", "남편분과 데이트하실 때를 떠올리시는군요. 주로 어디서 데이트하셨나요?"),
        ("user", "남산 타워에도 가고, 한강 둔치도 갔지"),
        ("ai", "그때는 어떤 계절이었나요? 날씨는 어땠어요?"),
        ("user", "봄이었어요. 벚꽃이 정말 예뻤지")
    ],
    [
        ("ai", "오늘 기분이 어떠세요? 무슨 생각을 하고 계셨어요?"),
        ("user", "옛날 직장 생활이 생각나네요"),
        ("ai", "어떤 일을 하셨나요? 직장 동료들은 어떠셨어요?"),
        ("user", "은행에서 일했는데, 동료들이 정말 좋았어요"),
        ("ai", "은행 일은 어떠셨나요? 어려운 점은 없으셨어요?"),
        ("user", "처음엔 어려웠는데 선배들이 잘 가르쳐줘서 금방 익혔어요"),
        ("ai", "점심시간에는 주로 무엇을 하셨나요?"),
        ("user", "근처 식당에서 동료들이랑 밥 먹고 산책도 했어요")
    ]
]

# 대화 요약 샘플
SUMMARY_TEMPLATES = [
    {
        "ai_summary": "오늘은 명동 거리에서의 추억을 이야기하셨습니다. 젊었을 때 친구들과 다방에서 커피를 마시고 영화관에 가셨던 즐거운 시간들을 떠올리셨습니다.",
        "mentioned_people": "순자(친구)",
        "main_topics": "명동 거리, 다방, 영화관, 친구",
        "emotional_tone": "즐거움, 그리움",
        "suggested_questions": "다방에서 친구들과 무슨 이야기를 나누셨나요? 명동에서 본 영화 중 기억에 남는 영화가 있나요?"
    },
    {
        "ai_summary": "학교 시절 담임선생님에 대한 따뜻한 추억을 나누셨습니다. 엄하지만 학생들을 진심으로 아끼셨던 선생님과 좋아했던 음악 시간에 대해 이야기하셨습니다.",
        "mentioned_people": "담임선생님",
        "main_topics": "학교, 선생님, 음악 시간, 노래",
        "emotional_tone": "감사함, 그리움",
        "suggested_questions": "음악 시간에 어떤 노래를 불렀나요? 학교 친구들과는 어떤 놀이를 하셨나요?"
    },
    {
        "ai_summary": "고향 전주에서의 추억을 회상하셨습니다. 특히 어머니와 함께 남부시장에 장 보러 가셨던 일상의 소중한 순간들을 떠올리셨습니다.",
        "mentioned_people": "어머니",
        "main_topics": "전주, 한옥마을, 남부시장, 콩나물국밥",
        "emotional_tone": "그리움, 따뜻함",
        "suggested_questions": "시장에서 산 재료로 어머니가 어떤 요리를 해주셨나요? 전주에서 제일 좋아했던 음식은 무엇인가요?"
    },
    {
        "ai_summary": "남편분과 데이트하셨던 봄날의 추억을 나누셨습니다. 이미자의 동백아가씨를 들으며 남산과 한강에서 보낸 로맨틱한 시간들을 회상하셨습니다.",
        "mentioned_people": "남편",
        "main_topics": "데이트, 남산, 한강, 벚꽃, 노래",
        "emotional_tone": "행복, 설렘, 그리움",
        "suggested_questions": "남편분과 처음 만나신 날은 어땠나요? 데이트 때 가장 기억에 남는 순간은 언제인가요?"
    },
    {
        "ai_summary": "은행에서 근무하셨던 직장 생활을 회상하셨습니다. 친절했던 동료들과 선배들, 함께 점심을 먹고 산책하던 일상의 소중한 순간들을 이야기하셨습니다.",
        "mentioned_people": "직장 동료들, 선배들",
        "main_topics": "은행, 직장 생활, 동료, 점심시간",
        "emotional_tone": "감사함, 즐거움",
        "suggested_questions": "은행에서 제일 기억에 남는 손님이 있으신가요? 퇴근 후에는 주로 무엇을 하셨나요?"
    }
]


def create_users():
    """더미 사용자 생성"""
    print("\n" + "=" * 50)
    print("📝 더미 사용자 생성 중...")
    print("=" * 50)
    
    user_ids = []
    
    for user_data in DUMMY_USERS:
        user_id = UserManager.create_user(**user_data)
        if user_id:
            user_ids.append(user_id)
            print(f"✅ {user_data['name']}님 생성 완료 (ID: {user_id})")
        else:
            print(f"❌ {user_data['name']}님 생성 실패")
    
    return user_ids


def create_conversations_and_messages(user_ids):
    """더미 대화 및 메시지 생성"""
    print("\n" + "=" * 50)
    print("💬 더미 대화 생성 중...")
    print("=" * 50)
    
    conversation_ids = []
    
    # 각 사용자마다 1-3개의 대화 생성
    for user_id in user_ids:
        user = UserManager.get_user_by_id(user_id)
        num_conversations = random.randint(1, 3)
        
        print(f"\n👤 {user['name']}님의 대화 생성 ({num_conversations}개)")
        
        for i in range(num_conversations):
            # 대화 세션 생성
            result = ChatManager.create_conversation(user_id)
            if not result:
                continue
            
            conversation_id, session_id = result
            conversation_ids.append(conversation_id)
            
            # 랜덤 대화 샘플 선택
            conversation_sample = random.choice(CONVERSATION_SAMPLES)
            
            # 메시지 추가
            for speaker, content in conversation_sample:
                ChatManager.add_message(conversation_id, speaker, content)
            
            # 대화 종료 (50% 확률)
            if random.random() > 0.5:
                ChatManager.end_conversation(conversation_id)
                status = "완료"
            else:
                status = "진행중"
            
            print(f"  ✅ 대화 #{i+1} 생성 완료 (ID: {conversation_id}, 메시지: {len(conversation_sample)}개, 상태: {status})")
    
    return conversation_ids


def create_summaries(conversation_ids):
    """더미 대화 요약 생성"""
    print("\n" + "=" * 50)
    print("📊 더미 요약 생성 중...")
    print("=" * 50)
    
    summary_count = 0
    
    for conversation_id in conversation_ids:
        # 완료된 대화만 요약 생성 (80% 확률)
        conversation = ChatManager.get_conversation_by_id(conversation_id)
        
        if conversation and conversation['status'] == '완료' and random.random() > 0.2:
            summary_template = random.choice(SUMMARY_TEMPLATES)
            
            summary_id = HistoryManager.create_summary(
                conversation_id,
                **summary_template
            )
            
            if summary_id:
                summary_count += 1
                print(f"✅ 대화 {conversation_id} 요약 생성 완료")
    
    print(f"\n총 {summary_count}개의 요약 생성 완료")


def create_past_conversations(user_ids):
    """과거 날짜의 대화 생성 (최근 7일)"""
    print("\n" + "=" * 50)
    print("📅 과거 대화 생성 중...")
    print("=" * 50)
    
    from database.db_config import get_connection, close_connection
    
    for user_id in user_ids:
        user = UserManager.get_user_by_id(user_id)
        
        # 최근 7일간 랜덤하게 대화 생성
        for days_ago in range(1, 8):
            # 30% 확률로 해당 날짜에 대화 생성
            if random.random() > 0.7:
                continue
            
            past_date = datetime.now() - timedelta(days=days_ago)
            
            # 대화 생성
            result = ChatManager.create_conversation(user_id)
            if not result:
                continue
            
            conversation_id, session_id = result
            
            # 과거 날짜로 변경
            connection = get_connection()
            cursor = connection.cursor()
            
            try:
                cursor.execute("""
                    UPDATE conversations 
                    SET start_time = %s, 
                        created_at = %s,
                        status = '완료',
                        end_time = %s,
                        duration = %s
                    WHERE id = %s
                """, (
                    past_date,
                    past_date,
                    past_date + timedelta(minutes=random.randint(5, 20)),
                    random.randint(300, 1200),
                    conversation_id
                ))
                connection.commit()
                
                # 메시지 추가
                conversation_sample = random.choice(CONVERSATION_SAMPLES)
                for idx, (speaker, content) in enumerate(conversation_sample):
                    msg_time = past_date + timedelta(minutes=idx)
                    
                    cursor.execute("""
                        INSERT INTO messages (conversation_id, speaker, content, timestamp)
                        VALUES (%s, %s, %s, %s)
                    """, (conversation_id, speaker, content, msg_time))
                
                connection.commit()
                
                # 요약 생성
                summary_template = random.choice(SUMMARY_TEMPLATES)
                cursor.execute("""
                    INSERT INTO summaries (conversation_id, ai_summary, mentioned_people, 
                                          main_topics, emotional_tone, suggested_questions)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    conversation_id,
                    summary_template['ai_summary'],
                    summary_template['mentioned_people'],
                    summary_template['main_topics'],
                    summary_template['emotional_tone'],
                    summary_template['suggested_questions']
                ))
                connection.commit()
                
                print(f"✅ {user['name']}님의 {days_ago}일 전 대화 생성 완료")
                
            finally:
                cursor.close()
                close_connection(connection)


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 70)
    print("🎉 기억상자 AI - 더미 데이터 생성 스크립트")
    print("=" * 70)
    
    try:
        # 1. 사용자 생성
        user_ids = create_users()
        
        if not user_ids:
            print("\n❌ 사용자 생성 실패. 스크립트를 종료합니다.")
            return
        
        # 2. 오늘 날짜 대화 생성
        conversation_ids = create_conversations_and_messages(user_ids)
        
        # 3. 요약 생성
        create_summaries(conversation_ids)
        
        # 4. 과거 대화 생성
        create_past_conversations(user_ids)
        
        # 통계 출력
        print("\n" + "=" * 70)
        print("📊 생성 완료 통계")
        print("=" * 70)
        print(f"✅ 총 사용자: {len(user_ids)}명")
        print(f"✅ 총 대화: {len(conversation_ids)}개 (오늘)")
        
        # 전체 통계 조회
        from database.db_config import fetch_one_dict
        
        total_stats = fetch_one_dict("""
            SELECT 
                COUNT(DISTINCT u.id) as total_users,
                COUNT(DISTINCT c.id) as total_conversations,
                COUNT(DISTINCT m.id) as total_messages,
                COUNT(DISTINCT s.id) as total_summaries
            FROM users u
            LEFT JOIN conversations c ON u.id = c.user_id
            LEFT JOIN messages m ON c.id = m.conversation_id
            LEFT JOIN summaries s ON c.id = s.conversation_id
        """)
        
        if total_stats:
            print(f"✅ 전체 대화: {total_stats['total_conversations']}개")
            print(f"✅ 전체 메시지: {total_stats['total_messages']}개")
            print(f"✅ 전체 요약: {total_stats['total_summaries']}개")
        
        print("\n" + "=" * 70)
        print("🎊 더미 데이터 생성 완료!")
        print("=" * 70)
        print("\n💡 이제 Streamlit 앱에서 데이터를 확인할 수 있습니다.")
        print("   streamlit run app.py\n")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
