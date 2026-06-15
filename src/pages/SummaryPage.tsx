import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '@/store/useStore';
import type { ChatMessage } from '@/store/useStore';

const SummaryPage: React.FC = () => {
  const navigate = useNavigate();
  const { chatMessages, clearMessages, guardianInfo } = useAppStore();

  // Demo messages if store is empty
  const demoMessages: ChatMessage[] = [
    {
      id: 'd1',
      role: 'ai',
      content: `안녕하세요 어르신 😊 오늘 날씨가 참 맑네요. 혹시 1960년대 짜장면 한 그릇이 15원~50원 정도 하던 시절 기억하시나요? 그때 자주 보시던 신문 광고나 정겨운 물가 소식이 있으신가요?`,
      timestamp: new Date(Date.now() - 120000),
    },
    {
      id: 'd2',
      role: 'user',
      content: `짜장면 곱빼기 배불리 먹던 날이 참 귀하고 좋았지. 삼양라면 처음 나왔을 때 먹었던 것도 기억나네.`,
      timestamp: new Date(Date.now() - 90000),
    },
    {
      id: 'd3',
      role: 'ai',
      content: `그러셨군요! 1960년대에는 '빨간 마후라'나 '미워도 다시 한번' 같은 신성일, 엄앵란 배우의 영화가 극장에서 정말 큰 인기를 끌었잖아요. 혹시 그때 극장에 가 보셨던 추억이나 유행했던 대중문화 소식이 생각나시나요?`,
      timestamp: new Date(Date.now() - 60000),
    },
    {
      id: 'd4',
      role: 'user',
      content: `극장 앞 매표소에 줄이 끝없이 서 있었어. 신성일 배우 보려고 영화 '미워도 다시 한번'을 보면서 친구들이랑 눈물 훔쳤던 기억이 나.`,
      timestamp: new Date(Date.now() - 30000),
    },
  ];

  const messagesToRender = chatMessages.length > 0 ? chatMessages : demoMessages;

  // Calculate stats
  const getStats = () => {
    if (chatMessages.length > 0) {
      const totalMessages = chatMessages.length;
      
      // Calculate duration
      const startTime = chatMessages[0].timestamp.getTime();
      const endTime = chatMessages[chatMessages.length - 1].timestamp.getTime();
      const diffSec = Math.max(10, Math.round((endTime - startTime) / 1000));
      
      const min = Math.floor(diffSec / 60);
      const sec = diffSec % 60;
      const durationStr = min > 0 ? `${min}분 ${sec}초` : `${sec}초`;
      
      // Calculate positive responses (user messages)
      const positiveCount = chatMessages.filter(m => m.role === 'user').length;
      
      return {
        total: `${totalMessages}번`,
        duration: durationStr,
        positive: `${positiveCount}개`
      };
    }
    
    // Default demo stats
    return {
      total: '4번',
      duration: '1분 48초',
      positive: '3개'
    };
  };

  const stats = getStats();

  const handleNewConversation = () => {
    clearMessages();
    navigate('/');
  };

  return (
    <div className="summary-container">
      <style>{`
        .summary-container {
          display: flex;
          flex-direction: column;
          min-height: 100vh;
          background-color: #FDF8F0;
          color: #3D2E1F;
          font-family: 'Noto Sans KR', sans-serif;
          box-sizing: border-box;
        }
        .summary-container * {
          box-sizing: border-box;
        }
        .summary-header {
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
          background: transparent;
          border: none;
          padding: 4px;
        }
        .summary-header-text {
          display: flex;
          flex-direction: column;
        }
        .summary-header-title {
          font-size: 18px;
          font-weight: 700;
          margin: 0;
        }
        .summary-header-subtitle {
          font-size: 13px;
          color: #8B7355;
          margin: 0;
        }
        .summary-body {
          flex-grow: 1;
          padding: 20px;
          max-width: 600px;
          margin: 0 auto;
          width: 100%;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        .stats-row {
          display: flex;
          gap: 12px;
        }
        .stat-card {
          flex: 1;
          background-color: #FFFFFF;
          border: 1px solid #E8DCC8;
          border-radius: 12px;
          padding: 14px;
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          gap: 6px;
          box-shadow: 0 2px 6px rgba(0,0,0,0.01);
        }
        .stat-icon {
          font-size: 24px;
        }
        .stat-value {
          font-size: 20px;
          font-weight: 700;
          color: #B8860B;
        }
        .stat-label {
          font-size: 12px;
          color: #8B7355;
        }
        .section-card {
          background-color: #FFFFFF;
          border: 1px solid #E8DCC8;
          border-radius: 16px;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 12px;
          box-shadow: 0 2px 6px rgba(0,0,0,0.01);
        }
        .section-title {
          font-size: 16px;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 6px;
          margin: 0;
          color: #3D2E1F;
          border-bottom: 2px solid #FDF8F0;
          padding-bottom: 8px;
        }
        .tag-container {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin-top: 4px;
        }
        .tag-chip {
          padding: 6px 14px;
          border-radius: 18px;
          font-size: 14px;
          font-weight: 700;
        }
        .tag-chip.place {
          background-color: #E3F2FD;
          color: #1976D2;
          border: 1px solid #BBDEFB;
        }
        .tag-chip.person {
          background-color: #E8F5E9;
          color: #388E3C;
          border: 1px solid #C8E6C9;
        }
        .bullet-list {
          margin: 0;
          padding-left: 20px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .bullet-list li {
          font-size: 15px;
          color: #3D2E1F;
          line-height: 1.4;
        }
        .numbered-list {
          margin: 0;
          padding-left: 20px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .numbered-list li {
          font-size: 15px;
          color: #3D2E1F;
          line-height: 1.4;
        }
        .history-container {
          display: flex;
          flex-direction: column;
          gap: 12px;
          max-height: 250px;
          overflow-y: auto;
          padding: 12px;
          background-color: #FDF8F0;
          border-radius: 12px;
          border: 1px solid #E8DCC8;
        }
        .history-row {
          display: flex;
          width: 100%;
        }
        .history-row.ai {
          justify-content: flex-start;
        }
        .history-row.user {
          justify-content: flex-end;
        }
        .history-bubble {
          padding: 10px 14px;
          border-radius: 14px;
          font-size: 14px;
          line-height: 1.4;
          max-width: 85%;
        }
        .history-row.ai .history-bubble {
          background-color: #FFF3E0;
          border: 1px solid #FFE0B2;
          color: #3D2E1F;
          border-radius: 0 14px 14px 14px;
        }
        .history-row.user .history-bubble {
          background-color: #F5F0E8;
          border: 1px solid #E8DCC8;
          color: #3D2E1F;
          border-radius: 14px 0 14px 14px;
        }
        .btn-restart-container {
          padding: 10px 0 40px 0;
        }
        .btn-restart {
          width: 100%;
          background: linear-gradient(135deg, #C49A3C 0%, #8B6914 100%);
          color: #FFFFFF;
          border: none;
          padding: 16px;
          border-radius: 12px;
          font-size: 18px;
          font-weight: 700;
          cursor: pointer;
          box-shadow: 0 6px 14px rgba(139, 105, 20, 0.3);
          transition: all 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
        }
        .btn-restart:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 18px rgba(139, 105, 20, 0.4);
        }
      `}</style>

      {/* Header Bar */}
      <header className="summary-header">
        <button className="home-icon" onClick={() => navigate('/')} aria-label="홈으로">🏠</button>
        <div className="summary-header-text">
          <h1 className="summary-header-title">오늘 대화 요약</h1>
          <p className="summary-header-subtitle">보호자님께 전달드리는 내용이에요</p>
        </div>
      </header>

      {/* Summary Contents */}
      <main className="summary-body">
        {/* Stats Row */}
        <div className="stats-row">
          <div className="stat-card">
            <span className="stat-icon">💬</span>
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">총 대화</span>
          </div>
          <div className="stat-card">
            <span className="stat-icon">⏱</span>
            <span className="stat-value">{stats.duration}</span>
            <span className="stat-label">대화 시간</span>
          </div>
          <div className="stat-card">
            <span className="stat-icon">😊</span>
            <span className="stat-value">{stats.positive}</span>
            <span className="stat-label">긍정 반응</span>
          </div>
        </div>

        {/* Places mentioned */}
        <div className="section-card">
          <h2 className="section-title">🏷 많이 나온 장소</h2>
          <div className="tag-container">
            <span className="tag-chip place">{guardianInfo.hometown ? guardianInfo.hometown : '동네 영화관'}</span>
            <span className="tag-chip place">동네 대포집</span>
            <span className="tag-chip place">완행열차 역</span>
          </div>
        </div>

        {/* People mentioned */}
        <div className="section-card">
          <h2 className="section-title">👥 언급된 인물</h2>
          <div className="tag-container">
            <span className="tag-chip person">신성일 배우</span>
            <span className="tag-chip person">학창시절 친구들</span>
            <span className="tag-chip person">어머니</span>
          </div>
        </div>

        {/* Positive topics */}
        <div className="section-card">
          <h2 className="section-title">🌟 긍정 반응한 주제</h2>
          <ul className="bullet-list">
            <li>
              1960년대 초반의 <strong>삼양라면과 짜장면 물가 소식</strong>에 대해 그 시절의 맛을 회상하며 매우 즐거워하셨습니다.
            </li>
            <li>
              당대 최고의 영화였던 <strong>'미워도 다시 한번'과 영화관 추억</strong>을 말씀하시며 촉촉해진 눈시울로 긍정적인 회상을 하셨습니다.
            </li>
            <li>
              검정 교복에 만원버스를 타던 <strong>학창시절의 정겨운 기억</strong>을 떠올리며 크게 웃으셨습니다.
            </li>
          </ul>
        </div>

        {/* Conversation Logs */}
        <div className="section-card">
          <h2 className="section-title">📋 전체 대화 기록</h2>
          <div className="history-container">
            {messagesToRender.map((msg) => (
              <div key={msg.id} className={`history-row ${msg.role}`}>
                <div className="history-bubble">
                  {msg.content}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Suggested next questions */}
        <div className="section-card">
          <h2 className="section-title">💡 다음에 이어갈 질문</h2>
          <ol className="numbered-list">
            <li>1960년대 명절 고향길 귀성 열차표를 구하기 위해 밤을 새우던 추억이나, 온 동네가 모여 명절을 보내던 모습은 어떠셨나요?</li>
            <li>검정 교복을 입고 다니던 중고등학교 학창 시절 운동회와 선생님의 추억을 더 나누어볼까요?</li>
            <li>어르신께서 1960년대에 가장 즐겨 들으셨던 애창곡(예: 이미자의 <strong>'{guardianInfo.favoriteSong ? guardianInfo.favoriteSong : '동백아가씨'}'</strong> 등)을 함께 들으며 노래에 얽힌 이야기를 나누어보시는 것도 좋겠습니다.</li>
          </ol>
        </div>

        {/* New Conversation Button */}
        <div className="btn-restart-container">
          <button className="btn-restart" onClick={handleNewConversation}>
            새 대화 시작하기 🔄
          </button>
        </div>
      </main>
    </div>
  );
};

export default SummaryPage;
