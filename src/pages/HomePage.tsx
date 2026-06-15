import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  // Get time-based greeting
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) {
      return '좋은 아침이에요 😊';
    } else if (hour < 18) {
      return '좋은 오후에요 😊';
    } else {
      return '좋은 저녁이에요 😊';
    }
  };

  return (
    <div className="home-container">
      <style>{`
        .home-container {
          display: flex;
          flex-direction: column;
          min-height: 100vh;
          background-color: #FDF8F0;
          color: #3D2E1F;
          font-family: 'Noto Sans KR', sans-serif;
        }
        .header-bar {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px 24px;
          background-color: #FFFFFF;
          border-bottom: 1px solid #E8DCC8;
          box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .header-left {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .header-logo {
          font-size: 28px;
        }
        .header-title-group {
          display: flex;
          flex-direction: column;
        }
        .header-title {
          font-size: 20px;
          font-weight: 700;
          margin: 0;
        }
        .header-subtitle {
          font-size: 14px;
          color: #8B7355;
          margin: 0;
        }
        .btn-guardian {
          border: 2px solid #B8860B;
          background: transparent;
          color: #B8860B;
          padding: 8px 16px;
          border-radius: 20px;
          font-size: 16px;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        .btn-guardian:hover {
          background-color: #B8860B;
          color: #FFFFFF;
        }
        .home-content {
          flex-grow: 1;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 40px 24px;
          text-align: center;
          gap: 32px;
        }
        .greeting {
          font-size: 22px;
          color: #8B7355;
          margin: 0;
          font-weight: 500;
        }
        .main-text {
          font-size: 34px;
          line-height: 1.5;
          font-weight: 700;
          margin: 0;
        }
        .main-text-highlight {
          color: #B8860B;
          font-size: 42px;
          font-weight: 900;
          display: inline-block;
          margin: 0 4px;
          border-bottom: 3px solid #E8DCC8;
        }
        .mic-button-wrapper {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 16px;
          margin: 20px 0;
        }
        .mic-button {
          width: 120px;
          height: 120px;
          border-radius: 50%;
          background: linear-gradient(135deg, #C49A3C 0%, #8B6914 100%);
          border: none;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          box-shadow: 0 8px 24px rgba(139, 105, 20, 0.3);
          transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
          position: relative;
        }
        .mic-button:hover {
          transform: scale(1.08);
          box-shadow: 0 12px 30px rgba(139, 105, 20, 0.4);
        }
        .mic-button::after {
          content: '';
          position: absolute;
          width: 100%;
          height: 100%;
          border-radius: 50%;
          border: 2px solid #C49A3C;
          animation: pulse 2s infinite;
          top: 0;
          left: 0;
          box-sizing: border-box;
        }
        @keyframes pulse {
          0% {
            transform: scale(1);
            opacity: 0.8;
          }
          100% {
            transform: scale(1.4);
            opacity: 0;
          }
        }
        .mic-icon-svg {
          width: 48px;
          height: 48px;
          fill: #FFFFFF;
        }
        .mic-instruction {
          font-size: 18px;
          color: #8B7355;
          margin: 0;
          font-weight: 500;
        }
        .bottom-area {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 16px;
          padding-bottom: 40px;
        }
        .summary-link-card {
          background-color: #FFFFFF;
          border: 1px solid #E8DCC8;
          border-radius: 12px;
          padding: 14px 28px;
          cursor: pointer;
          text-decoration: none;
          color: #3D2E1F;
          font-weight: 700;
          font-size: 18px;
          box-shadow: 0 4px 6px rgba(0,0,0,0.02);
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .summary-link-card:hover {
          border-color: #B8860B;
          box-shadow: 0 6px 12px rgba(184, 134, 11, 0.1);
        }
        .footer-text {
          font-size: 14px;
          color: #8B7355;
          margin: 0;
        }
      `}</style>

      {/* Header Bar */}
      <header className="header-bar">
        <div className="header-left">
          <span className="header-logo">📦</span>
          <div className="header-title-group">
            <h1 className="header-title">기억상자 AI</h1>
            <p className="header-subtitle">추억을 꺼내는 대화</p>
          </div>
        </div>
        <button className="btn-guardian" onClick={() => navigate('/guardian-info')}>
          보호자 설정
        </button>
      </header>

      {/* Main Content */}
      <main className="home-content">
        <p className="greeting">{getGreeting()}</p>
        <h2 className="main-text">
          오늘은 어떤<br />
          <span className="main-text-highlight">추억</span>을<br />
          이야기할까요?
        </h2>

        <div className="mic-button-wrapper">
          <button className="mic-button" onClick={() => navigate('/chat')} aria-label="음성 대화 시작">
            {/* SVG Microphone Icon */}
            <svg className="mic-icon-svg" viewBox="0 0 24 24">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z" />
            </svg>
          </button>
          <p className="mic-instruction">버튼을 누르고 말씀해 주세요</p>
        </div>
      </main>

      {/* Bottom Area */}
      <footer className="bottom-area">
        <div className="summary-link-card" onClick={() => navigate('/history')}>
          📋 이전 대화 기록 보기 &gt;
        </div>
        <p className="footer-text">편하게 말씀하시면 AI가 함께 이야기 나눠드립니다</p>
      </footer>
    </div>
  );
};

export default HomePage;
