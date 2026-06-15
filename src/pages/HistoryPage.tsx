import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '@/store/useStore';

interface HistoryItem {
  id: string;
  date: string;
  time: string;
  duration: string;
  responses: number;
  tags: string[];
  summary: string;
  places: string[];
  people: string[];
  positiveTopics: string[];
  nextQuestions: string[];
  messages: {
    role: 'ai' | 'user';
    content: string;
    positiveBadge?: boolean;
  }[];
}

const HistoryPage: React.FC = () => {
  const navigate = useNavigate();
  const { guardianInfo } = useAppStore();

  const [expandedId, setExpandedId] = useState<string | null>('h2'); // Default to expand June 7 (as in Image 2)
  const [activeTabs, setActiveTabs] = useState<Record<string, 'summary' | 'chat'>>({
    h1: 'summary',
    h2: 'summary',
    h3: 'summary',
  });

  const historyData: HistoryItem[] = [
    {
      id: 'h1',
      date: '2026년 6월 9일',
      time: '14:30',
      duration: '12분 12초',
      responses: 4,
      tags: ['시장 음식 이야기', '어머니와의 추억', '이미자 노래'],
      summary: `오늘 어르신은 1960년대 고향 시장에서 어머니와 함께했던 따뜻한 장보기의 추억을 나누었습니다. 삼양라면이 처음 출시되었을 때의 신기했던 감정, 그리고 시장 골목에서 들려오던 라디오 속 이미자 가수의 목소리를 또렷이 기억해내셨습니다. 대화 전반에서 따뜻함과 그리움이 가득 느껴졌습니다.`,
      places: [guardianInfo.hometown ? `${guardianInfo.hometown} 시장` : '군산 시장', '시장 골목길'],
      people: ['어머니', '이미자 가수'],
      positiveTopics: ['시장 음식 이야기', '어머니와의 추억', '이미자 노래'],
      nextQuestions: [
        '어머니와 함께 시장에서 샀던 물건 중 가장 기억에 남는 것이 있으신가요?',
        '이미자 가수의 노래 중 가장 즐겨 부르시던 노래는 무엇인가요?',
        '시장 골목에서 풍기던 음식 냄새 중 어떤 냄새가 가장 그리우신가요?',
      ],
      messages: [
        { role: 'ai', content: '안녕하세요 어르신 😊 오늘 날씨가 참 맑네요. 혹시 1960년대 짜장면 한 그릇이 15원~50원 정도 하던 시절 기억하시나요? 그때 자주 보시던 신문 광고나 정겨운 물가 소식이 있으신가요?' },
        { role: 'user', content: '짜장면 곱빼기 배불리 먹던 날이 참 귀하고 좋았지. 삼양라면 처음 나왔을 때 먹었던 것도 기억나네.', positiveBadge: true },
        { role: 'ai', content: '그러셨군요! 그 시장에서 어떤 음식을 제일 즐겨 드셨나요? 생각이 나지 않으셔도 괜찮아요 😊' },
        { role: 'user', content: '거기서 파는 뜨끈한 칼국수가 참 맛있었어. 어머니랑 시장 갈 때마다 사달라고 떼썼지.', positiveBadge: true },
        { role: 'ai', content: '어머, 정말 맛있겠어요 😋 그때 누구랑 같이 가셨어요? 그때 분위기는 어땠나요?' },
        { role: 'user', content: '어머니 손 꼭 잡고 시장 골목골목을 구경했어. 이미자 노래가 라디오에서 작게 흘러나오던 기억이 나네.', positiveBadge: true },
        { role: 'ai', content: '어르신의 따뜻한 추억이 정말 아름답네요. 들려주셔서 감사합니다! 😊' },
        { role: 'user', content: '오늘 참 재밌었어 고마워.' },
      ],
    },
    {
      id: 'h2',
      date: '2026년 6월 7일',
      time: '10:15',
      duration: '8분 0초',
      responses: 3,
      tags: ['교직 시절 이야기', '아이들과의 추억', '학교 생활'],
      summary: `오늘 어르신은 초등학교 교사로 근무하셨던 시절, 특히 운동장에서 아이들이 뛰어노는 모습을 회상하셨습니다. 국어 과목을 가르치셨으며 학생들을 매우 사랑하셨던 것이 느껴졌습니다. 직업과 교직 경험에 대한 이야기가 자연스럽고 밝게 이어졌습니다.`,
      places: ['학교 운동장', '군산'],
      people: ['학생들'],
      positiveTopics: ['교직 시절 이야기', '아이들과의 추억', '학교 생활'],
      nextQuestions: [
        '가장 기억에 남는 학생이 있으셨나요?',
        '학교 소풍이나 운동회는 어떻게 진행됐나요?',
        '선생님이 되신 계기가 있으셨나요?',
      ],
      messages: [
        { role: 'ai', content: '안녕하세요 어르신 😊 오늘은 어떤 이야기를 나눠볼까요?' },
        { role: 'user', content: '학교 운동장이 생각나네', positiveBadge: true },
        { role: 'ai', content: '학교 운동장이요! 그때 분위기는 어땠나요?' },
        { role: 'user', content: '아이들이 뛰어노는 소리가 참 좋았어', positiveBadge: true },
        { role: 'ai', content: '선생님으로 계실 때 이야기인가요? 어떤 과목을 가르치셨어요?' },
        { role: 'user', content: '국어를 가르쳤어. 애들이 참 귀여웠지', positiveBadge: true },
      ],
    },
    {
      id: 'h3',
      date: '2026년 6월 5일',
      time: '16:00',
      duration: '6분 0초',
      responses: 3,
      tags: ['흑백영화 관람', '친구들과의 추억', '나그네 영화'],
      summary: `오늘 어르신은 1960년대 동네 극장에서 친구들과 함께 흑백영화 '나그네'를 보셨던 추억을 회상하셨습니다. 매표소 앞의 긴 줄과 영화를 보며 눈물짓던 기억에 대해 긍정적인 반응을 보이셨습니다. 대중문화와 과거 여가 활동을 떠올리며 정서적인 환기를 하셨습니다.`,
      places: ['동네 극장', '매표소 앞'],
      people: ['학창시절 친구들', '영화배우'],
      positiveTopics: ['흑백영화 관람', '친구들과의 추억', '나그네 영화'],
      nextQuestions: [
        '그 시절 가장 좋아하던 영화배우는 누구였나요?',
        '친구들과 영화관을 간 뒤에는 주로 무엇을 하셨나요?',
        '영화표 가격은 얼마였는지 기억나시나요?',
      ],
      messages: [
        { role: 'ai', content: '안녕하세요 어르신 😊 오늘 날씨가 참 맑네요. 혹시 1960년대 동네 극장에 자주 가셨나요?' },
        { role: 'user', content: '영화관에서 친구들과 흑백영화 보던 게 생각나', positiveBadge: true },
        { role: 'ai', content: '어머나, 친구분들과 어떤 영화를 보셨어요?' },
        { role: 'user', content: '나그네라는 영화를 보면서 많이들 울었지', positiveBadge: true },
        { role: 'ai', content: '그때 극장 주변 분위기는 어땠나요? 사람들이 많았나요?' },
        { role: 'user', content: '매표소 앞에 줄이 끝도 없었어. 시끌벅적하니 재밌었지', positiveBadge: true },
      ],
    },
  ];

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const handleTabChange = (id: string, tab: 'summary' | 'chat') => {
    setActiveTabs((prev) => ({ ...prev, [id]: tab }));
  };

  return (
    <div className="history-page-container">
      <style>{`
        .history-page-container {
          display: flex;
          flex-direction: column;
          min-height: 100vh;
          background-color: #FDF8F0;
          color: #3D2E1F;
          font-family: 'Noto Sans KR', sans-serif;
          box-sizing: border-box;
        }
        .history-page-container * {
          box-sizing: border-box;
        }
        .history-header {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 16px 20px;
          background-color: #FFFFFF;
          border-bottom: 1px solid #E8DCC8;
        }
        .home-icon {
          font-size: 24px;
          cursor: pointer;
          background: #F5E6C8;
          border: none;
          padding: 8px 10px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background-color 0.2s;
        }
        .home-icon:hover {
          background-color: #E8DCC8;
        }
        .history-header-text {
          display: flex;
          flex-direction: column;
        }
        .history-header-title {
          font-size: 18px;
          font-weight: 700;
          margin: 0;
        }
        .history-header-subtitle {
          font-size: 13px;
          color: #8B7355;
          margin: 0;
        }
        .history-body {
          flex-grow: 1;
          padding: 20px;
          max-width: 960px;
          margin: 0 auto;
          width: 100%;
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        .history-card {
          background-color: #FFFFFF;
          border: 1px solid #E8DCC8;
          border-radius: 20px;
          overflow: hidden;
          box-shadow: 0 4px 10px rgba(0,0,0,0.01);
          transition: box-shadow 0.2s;
        }
        .history-card.expanded {
          box-shadow: 0 8px 20px rgba(139, 105, 20, 0.05);
        }
        .card-header-clickable {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 20px;
          cursor: pointer;
          user-select: none;
        }
        .card-header-left {
          display: flex;
          align-items: center;
          gap: 14px;
        }
        .bubble-icon-wrapper {
          width: 44px;
          height: 44px;
          background-color: #F5F0E8;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 20px;
        }
        .card-header-info {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }
        .card-date {
          font-size: 18px;
          font-weight: 700;
          margin: 0;
          color: #3D2E1F;
        }
        .card-meta {
          font-size: 13px;
          color: #8B7355;
          margin: 0;
        }
        .card-header-right {
          font-size: 14px;
          color: #B8860B;
          display: flex;
          align-items: center;
        }
        .arrow-icon {
          transition: transform 0.2s;
          font-size: 12px;
        }
        .arrow-icon.down {
          transform: rotate(0deg);
        }
        .arrow-icon.up {
          transform: rotate(180deg);
        }
        .card-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          padding: 0 20px 20px 78px;
          margin-top: -6px;
        }
        .card-tag {
          background-color: #FFF9F0;
          color: #B8860B;
          border: 1px solid #E8DCC8;
          padding: 4px 10px;
          border-radius: 12px;
          font-size: 13px;
          font-weight: 700;
        }
        .card-expanded-content {
          border-top: 1px solid #F0E8D8;
          background-color: #FFFFFF;
        }
        .tabs-row {
          display: flex;
          border-bottom: 1px solid #E8DCC8;
          background-color: #FFFFFF;
        }
        .tab-btn {
          flex: 1;
          background: transparent;
          border: none;
          padding: 14px;
          font-size: 16px;
          font-weight: 700;
          color: #8B7355;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          position: relative;
        }
        .tab-btn.active {
          color: #B8860B;
        }
        .tab-btn.active::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 0;
          width: 100%;
          height: 3px;
          background-color: #B8860B;
        }
        .tab-pane {
          padding: 24px;
          display: flex;
          flex-direction: column;
          gap: 20px;
          background-color: #FFFFFF;
        }
        .ai-summary-box {
          background-color: #F9F6F0;
          border: 1px solid #E8DCC8;
          border-radius: 12px;
          padding: 16px 20px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .summary-box-title {
          font-weight: 700;
          font-size: 14px;
          color: #8B7355;
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .summary-box-content {
          font-size: 15px;
          line-height: 1.6;
          color: #3D2E1F;
          margin: 0;
        }
        .mentions-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }
        .mentions-card {
          background-color: #FAF6EE;
          border: 1px solid #E8DCC8;
          border-radius: 12px;
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .mentions-title {
          font-size: 14px;
          font-weight: 700;
          color: #3D2E1F;
          display: flex;
          align-items: center;
          gap: 6px;
          margin: 0;
        }
        .mentions-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
        }
        .tag-chip {
          padding: 4px 10px;
          border-radius: 12px;
          font-size: 13px;
          font-weight: 700;
        }
        .tag-chip.blue {
          background-color: #E3F2FD;
          color: #1976D2;
          border: 1px solid #BBDEFB;
        }
        .tag-chip.purple {
          background-color: #F3E5F5;
          color: #7B1FA2;
          border: 1px solid #E1BEE7;
        }
        .tag-chip.gold {
          background-color: #FFF9F0;
          color: #B8860B;
          border: 1px solid #E8DCC8;
        }
        .numbered-question-card {
          background-color: #FAF6EE;
          border: 1px solid #E8DCC8;
          border-radius: 12px;
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 12px;
        }
        .questions-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .question-item {
          display: flex;
          align-items: flex-start;
          gap: 10px;
          font-size: 15px;
          line-height: 1.5;
          color: #3D2E1F;
        }
        .question-number {
          background-color: #F5E6C8;
          color: #B8860B;
          font-weight: 700;
          font-size: 12px;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          margin-top: 2px;
        }
        .chat-history-list {
          display: flex;
          flex-direction: column;
          gap: 16px;
          background-color: #FFFFFF;
        }
        .chat-history-row {
          display: flex;
          width: 100%;
        }
        .chat-history-row.ai {
          justify-content: flex-start;
        }
        .chat-history-row.user {
          justify-content: flex-end;
          align-items: center;
          gap: 8px;
        }
        .avatar-wrap {
          font-size: 20px;
          margin-right: 8px;
          align-self: flex-start;
          margin-top: 4px;
        }
        .history-bubble-inner {
          padding: 12px 16px;
          line-height: 1.5;
          font-size: 15px;
          max-width: 80%;
          box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .chat-history-row.ai .history-bubble-inner {
          background-color: #FFF3E0;
          border: 1px solid #FFE0B2;
          color: #3D2E1F;
          border-radius: 0 16px 16px 16px;
        }
        .chat-history-row.user .history-bubble-inner {
          background-color: #F5F0E8;
          border: 1px solid #E8DCC8;
          color: #3D2E1F;
          border-radius: 16px 0 16px 16px;
        }
        .reaction-badge {
          width: 20px;
          height: 20px;
          background-color: #B8860B;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 10px;
          color: #FFFFFF;
          box-shadow: 0 2px 4px rgba(184,134,11,0.3);
          flex-shrink: 0;
        }
      `}</style>

      {/* Header Bar */}
      <header className="history-header">
        <button className="home-icon" onClick={() => navigate('/')} aria-label="홈으로">
          🏠
        </button>
        <div className="history-header-text">
          <h1 className="history-header-title">이전 대화 기록</h1>
          <p className="history-header-subtitle">총 {historyData.length}번의 대화</p>
        </div>
      </header>

      {/* Body List */}
      <main className="history-body">
        {historyData.map((item) => {
          const isExpanded = expandedId === item.id;
          const activeTab = activeTabs[item.id] || 'summary';

          return (
            <div key={item.id} className={`history-card ${isExpanded ? 'expanded' : ''}`}>
              {/* Clickable Header */}
              <div className="card-header-clickable" onClick={() => toggleExpand(item.id)}>
                <div className="card-header-left">
                  <div className="bubble-icon-wrapper">💬</div>
                  <div className="card-header-info">
                    <h2 className="card-date">{item.date}</h2>
                    <p className="card-meta">
                      {item.time} · {item.duration} · {item.responses}번 응답
                    </p>
                  </div>
                </div>
                <div className="card-header-right">
                  <span className={`arrow-icon ${isExpanded ? 'up' : 'down'}`}>
                    ▼
                  </span>
                </div>
              </div>

              {/* Tags under header */}
              <div className="card-tags">
                {item.tags.map((tag, idx) => (
                  <span key={idx} className="card-tag">
                    {tag}
                  </span>
                ))}
              </div>

              {/* Expanded Area */}
              {isExpanded && (
                <div className="card-expanded-content">
                  {/* Tabs */}
                  <div className="tabs-row">
                    <button
                      className={`tab-btn ${activeTab === 'summary' ? 'active' : ''}`}
                      onClick={() => handleTabChange(item.id, 'summary')}
                    >
                      📄 요약
                    </button>
                    <button
                      className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
                      onClick={() => handleTabChange(item.id, 'chat')}
                    >
                      💬 전체 대화
                    </button>
                  </div>

                  {/* Tab Pane */}
                  {activeTab === 'summary' ? (
                    <div className="tab-pane">
                      {/* AI Summary */}
                      <div className="ai-summary-box">
                        <div className="summary-box-title">
                          🤖 AI 요약
                        </div>
                        <p className="summary-box-content">{item.summary}</p>
                      </div>

                      {/* Mentions Grid */}
                      <div className="mentions-grid">
                        <div className="mentions-card">
                          <h3 className="mentions-title">📍 언급된 장소</h3>
                          <div className="mentions-tags">
                            {item.places.map((place, i) => (
                              <span key={i} className="tag-chip blue">
                                {place}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div className="mentions-card">
                          <h3 className="mentions-title">👥 언급된 인물</h3>
                          <div className="mentions-tags">
                            {item.people.map((person, i) => (
                              <span key={i} className="tag-chip purple">
                                {person}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* Positive reaction topics */}
                      <div className="mentions-card">
                        <h3 className="mentions-title">😊 긍정 반응 주제</h3>
                        <div className="mentions-tags">
                          {item.positiveTopics.map((topic, i) => (
                            <span key={i} className="tag-chip gold">
                              {topic}
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* Next Questions */}
                      <div className="numbered-question-card">
                        <h3 className="mentions-title">💡 다음에 이어갈 질문</h3>
                        <div className="questions-list">
                          {item.nextQuestions.map((q, i) => (
                            <div key={i} className="question-item">
                              <span className="question-number">{i + 1}</span>
                              <span>{q}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="tab-pane">
                      {/* Chat History View */}
                      <div className="chat-history-list">
                        {item.messages.map((msg, i) => (
                          <div key={i} className={`chat-history-row ${msg.role}`}>
                            {msg.role === 'ai' && (
                              <span className="avatar-wrap">🤖</span>
                            )}
                            <div className="history-bubble-inner">
                              {msg.content}
                            </div>
                            {msg.role === 'user' && msg.positiveBadge && (
                              <span className="reaction-badge" title="긍정 반응 감지">⭐</span>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </main>
    </div>
  );
};

export default HistoryPage;
