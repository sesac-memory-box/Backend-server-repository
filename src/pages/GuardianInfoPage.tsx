import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '@/store/useStore';
import type { GuardianInfo } from '@/store/useStore';

const GuardianInfoPage: React.FC = () => {
  const navigate = useNavigate();
  const { guardianInfo, setGuardianInfo } = useAppStore();

  const [formData, setFormData] = useState<GuardianInfo>({
    hometown: guardianInfo.hometown || '',
    pastJob: guardianInfo.pastJob || '',
    favoriteFood: guardianInfo.favoriteFood || '',
    memoryPlace: guardianInfo.memoryPlace || '',
    favoriteSong: guardianInfo.favoriteSong || '',
    sensitiveTopics: guardianInfo.sensitiveTopics || '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setGuardianInfo(formData);
    navigate('/');
  };

  return (
    <div className="guardian-container">
      <style>{`
        .guardian-container {
          display: flex;
          flex-direction: column;
          min-height: 100vh;
          background-color: #FDF8F0;
          color: #3D2E1F;
          font-family: 'Noto Sans KR', sans-serif;
          box-sizing: border-box;
        }
        .guardian-container * {
          box-sizing: border-box;
        }
        .guardian-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px 20px;
          background-color: #FFFFFF;
          border-bottom: 1px solid #E8DCC8;
        }
        .guardian-header-left {
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .home-icon {
          font-size: 26px;
          cursor: pointer;
          background: transparent;
          border: none;
          padding: 4px;
        }
        .guardian-header-text {
          display: flex;
          flex-direction: column;
        }
        .guardian-header-title {
          font-size: 18px;
          font-weight: 700;
          margin: 0;
        }
        .guardian-header-subtitle {
          font-size: 13px;
          color: #8B7355;
          margin: 0;
        }
        .btn-cancel {
          background: transparent;
          border: none;
          color: #8B7355;
          font-weight: 700;
          font-size: 16px;
          cursor: pointer;
          padding: 6px;
        }
        .guardian-body {
          flex-grow: 1;
          padding: 20px;
          max-width: 600px;
          margin: 0 auto;
          width: 100%;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        .notice-banner {
          background-color: #FFF9E6;
          border: 1px solid #FFE0B2;
          border-radius: 12px;
          padding: 16px;
          display: flex;
          gap: 12px;
          align-items: flex-start;
        }
        .notice-emoji {
          font-size: 22px;
        }
        .notice-text {
          font-size: 14px;
          color: #8B7355;
          line-height: 1.6;
          margin: 0;
        }
        .form-card {
          background-color: #FFFFFF;
          border: 1px solid #E8DCC8;
          border-radius: 16px;
          padding: 24px;
          display: flex;
          flex-direction: column;
          gap: 20px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.01);
        }
        .form-field {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .field-label {
          display: flex;
          align-items: center;
          gap: 6px;
          font-weight: 700;
          font-size: 16px;
          color: #3D2E1F;
        }
        .field-input {
          background-color: #FDF8F0;
          border: 1px solid #E8DCC8;
          border-radius: 8px;
          padding: 12px 14px;
          font-size: 16px;
          outline: none;
          color: #3D2E1F;
          font-family: inherit;
          transition: border-color 0.2s;
          width: 100%;
        }
        .field-input:focus {
          border-color: #B8860B;
          background-color: #FFFFFF;
        }
        .field-textarea {
          min-height: 100px;
          resize: vertical;
        }
        .btn-save-container {
          padding: 10px 0 40px 0;
        }
        .btn-save {
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
        }
        .btn-save:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 18px rgba(139, 105, 20, 0.4);
        }
      `}</style>

      {/* Header Bar */}
      <header className="guardian-header">
        <div className="guardian-header-left">
          <button className="home-icon" onClick={() => navigate('/')} aria-label="홈으로">🏠</button>
          <div className="guardian-header-text">
            <h1 className="guardian-header-title">보호자 정보 입력</h1>
            <p className="guardian-header-subtitle">어르신 맞춤 대화를 위한 정보에요</p>
          </div>
        </div>
        <button className="btn-cancel" onClick={() => navigate('/')}>
          취소
        </button>
      </header>

      {/* Notice Banner & Form */}
      <main className="guardian-body">
        <div className="notice-banner">
          <span className="notice-emoji">⚡</span>
          <p className="notice-text">
            입력하신 정보는 AI 대화에만 활용되며, 외부로 전송되거나 저장되지 않습니다. 
            어르신의 삶에 가까운 이야기로 대화를 나눌 수 있어요.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="form-card">
          <div className="form-field">
            <label className="field-label">
              <span>🏡</span> 고향
            </label>
            <input
              type="text"
              name="hometown"
              className="field-input"
              placeholder="예) 전라북도 군산"
              value={formData.hometown}
              onChange={handleChange}
            />
          </div>

          <div className="form-field">
            <label className="field-label">
              <span>💼</span> 과거 직업
            </label>
            <input
              type="text"
              name="pastJob"
              className="field-input"
              placeholder="예) 초등학교 교사, 농사일"
              value={formData.pastJob}
              onChange={handleChange}
            />
          </div>

          <div className="form-field">
            <label className="field-label">
              <span>🍲</span> 좋아하는 음식
            </label>
            <input
              type="text"
              name="favoriteFood"
              className="field-input"
              placeholder="예) 칼국수, 김치전, 삼계탕"
              value={formData.favoriteFood}
              onChange={handleChange}
            />
          </div>

          <div className="form-field">
            <label className="field-label">
              <span>📍</span> 추억의 장소
            </label>
            <input
              type="text"
              name="memoryPlace"
              className="field-input"
              placeholder="예) 군산 시장, 학교 운동장"
              value={formData.memoryPlace}
              onChange={handleChange}
            />
          </div>

          <div className="form-field">
            <label className="field-label">
              <span>🎵</span> 좋아했던 노래 / 가수
            </label>
            <input
              type="text"
              name="favoriteSong"
              className="field-input"
              placeholder="예) 이미자, 나훈아, 조용필"
              value={formData.favoriteSong}
              onChange={handleChange}
            />
          </div>

          <div className="form-field">
            <label className="field-label">
              <span>⚠️</span> 주의할 주제 (민감한 사항)
            </label>
            <textarea
              name="sensitiveTopics"
              className="field-input field-textarea"
              placeholder="예) 돌아가신 배우자 이야기는 조심스럽게 꺼내주세요."
              value={formData.sensitiveTopics}
              onChange={handleChange}
            />
          </div>

          <div className="btn-save-container">
            <button type="submit" className="btn-save">
              저장하고 돌아가기 ✓
            </button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default GuardianInfoPage;
