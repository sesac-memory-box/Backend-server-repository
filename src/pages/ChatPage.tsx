import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '@/store/useStore';
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition';
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis';

const ChatPage: React.FC = () => {
  const navigate = useNavigate();
  const {
    chatMessages,
    addMessage,
    settings,
    updateSettings,
    guardianInfo,
  } = useAppStore();

  const {
    transcript,
    interimTranscript,
    isListening,
    startListening,
    stopListening,
    resetTranscript,
  } = useSpeechRecognition();

  const {
    speak,
    cancel: cancelTts,
    isSpeaking,
    getKoreanVoices,
  } = useSpeechSynthesis();

  const [inputValue, setInputValue] = useState('');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Sync speech transcript to input field
  useEffect(() => {
    if (transcript) {
      setInputValue(transcript);
    }
  }, [transcript]);

  // Handle voice speech and auto-focus/auto-trigger
  const speakMessage = (text: string) => {
    if (!settings.ttsEnabled) return;
    
    // Choose speech rate
    let rate = 1.0;
    if (settings.speechRate === 'slow') rate = 0.7;
    if (settings.speechRate === 'fast') rate = 1.3;

    // Resolve voiceURI
    const koVoices = getKoreanVoices();
    let voiceURI = undefined;
    if (koVoices.length > 0) {
      if (settings.ttsVoice === 'female2' && koVoices[1]) {
        voiceURI = koVoices[1].voiceURI;
      } else if (settings.ttsVoice === 'male1' && koVoices[2]) {
        voiceURI = koVoices[2].voiceURI;
      } else if (settings.ttsVoice === 'male2' && koVoices[3]) {
        voiceURI = koVoices[3].voiceURI;
      } else {
        voiceURI = koVoices[0].voiceURI;
      }
    }

    speak(text, { rate, voiceURI });
  };

  // Scroll to bottom whenever messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  // Initial prompt setup
  useEffect(() => {
    if (chatMessages.length === 0) {
      const hometownInfo = guardianInfo.hometown ? `고향인 ${guardianInfo.hometown} 소식이나 ` : '';
      const initialGreeting = `안녕하세요 어르신 😊 오늘 날씨가 참 맑네요. 혹시 1960년대 짜장면 한 그릇이 15원~50원 정도 하던 시절 기억하시나요? ${hometownInfo}그때 자주 보시던 신문 광고나 정겨운 물가 소식이 있으신가요?`;
      addMessage({ role: 'ai', content: initialGreeting });
      
      // Delay speak slightly to allow browser SpeechSynthesis to load
      setTimeout(() => {
        speakMessage(initialGreeting);
      }, 500);
    }
  }, []);

  // Stop STT when AI is speaking, and restart afterwards
  useEffect(() => {
    if (isSpeaking && isListening) {
      stopListening();
    }
  }, [isSpeaking]);

  // Pre-scripted AI conversation simulator
  const handleUserResponse = (text: string) => {
    if (!text.trim()) return;

    // Add user message
    addMessage({ role: 'user', content: text });
    setInputValue('');
    resetTranscript();
    cancelTts();

    // Determine the next AI response
    // Calculate how many user messages are currently in the chat
    const userMessageCount = chatMessages.filter(m => m.role === 'user').length + 1;

    setTimeout(() => {
      let aiText = '';
      if (userMessageCount === 1) {
        aiText = `그러셨군요! 1960년대에는 '빨간 마후라'나 '미워도 다시 한번' 같은 신성일, 엄앵란 배우의 영화가 극장에서 정말 큰 인기를 끌었잖아요. 혹시 그때 극장에 가 보셨던 추억이나 유행했던 대중문화 소식이 생각나시나요?`;
      } else if (userMessageCount === 2) {
        aiText = `정말 그리운 기억이네요! 스포츠로는 김기수 권투 선수나 라디오로 들었던 고교야구 소식으로 온 나라가 들썩였는데요. 어르신의 학창 시절 운동회 때나 학교 갈 때 완행열차, 만원버스를 타던 추억도 생각나시나요?`;
      } else {
        aiText = `어르신과 얘기하니 1960년대의 정겨운 풍경이 머릿속에 그대로 그려지는 것 같아요. 검정 교복, 새해 설날이나 추석 명절에 가득 찼던 귀성 열차의 설렘까지 모두 소중한 인생의 보물입니다. 오늘 정겨운 추억 들려주셔서 정말 감사해요 어르신! 😊`;
      }

      addMessage({ role: 'ai', content: aiText });
      speakMessage(aiText);
    }, 1500);
  };

  // Quick replies configuration
  const getQuickReplies = () => {
    const userMsgCount = chatMessages.filter(m => m.role === 'user').length;
    
    if (userMsgCount === 0) {
      const town = guardianInfo.hometown ? `${guardianInfo.hometown} 시장` : '동네 시장';
      return [
        `짜장면 곱빼기 먹던 날이 최고였지`,
        `삼양라면 처음 나왔을 때 참 신기했어`,
        `${town}에서 사 먹던 물가가 아직도 생각나`
      ];
    } else if (userMsgCount === 1) {
      return [
        "미워도 다시 한번 보고 정말 많이 울었지",
        "동네 극장에 온 동네 사람들이 모이던 때였어",
        "신성일, 엄앵란 배우가 단연 최고 인기가수였지"
      ];
    } else if (userMsgCount === 2) {
      return [
        "청군 이겨라! 백군 이겨라! 운동회는 온 동네 축제였어",
        "김기수 챔피언 경기 때 라디오 앞에 다닥다닥 모였었지",
        "검정 교복에 만원버스, 전차 타던 시절이 눈에 선해"
      ];
    } else {
      return ["대화 종료하고 요약 보기"];
    }
  };

  const toggleMic = () => {
    if (isListening) {
      stopListening();
      if (inputValue.trim()) {
        handleUserResponse(inputValue);
      }
    } else {
      cancelTts();
      resetTranscript();
      setInputValue('');
      startListening();
    }
  };

  // Resolve font size class
  const getFontSizeClass = () => {
    if (settings.fontSize === 'xlarge') return 'font-size-xlarge';
    if (settings.fontSize === 'large') return 'font-size-large';
    return 'font-size-default';
  };

  return (
    <div className={`chat-container ${getFontSizeClass()}`}>
      <style>{`
        .chat-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background-color: #FDF8F0;
          color: #3D2E1F;
          font-family: 'Noto Sans KR', sans-serif;
          position: relative;
          overflow: hidden;
          box-sizing: border-box;
        }
        .chat-container * {
          box-sizing: border-box;
        }
        .font-size-default { font-size: 18px; }
        .font-size-large { font-size: 22px; }
        .font-size-xlarge { font-size: 26px; }

        .chat-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px 20px;
          background-color: #FFFFFF;
          border-bottom: 1px solid #E8DCC8;
          z-index: 10;
        }
        .header-info {
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .header-emoji {
          font-size: 24px;
        }
        .header-text {
          display: flex;
          flex-direction: column;
        }
        .header-title {
          font-size: 18px;
          font-weight: 700;
          margin: 0;
        }
        .header-subtitle {
          font-size: 13px;
          color: #8B7355;
          margin: 0;
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .status-dot {
          width: 8px;
          height: 8px;
          background-color: #4CAF50;
          border-radius: 50%;
          display: inline-block;
        }
        .header-actions {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .btn-settings {
          background: transparent;
          border: none;
          font-size: 24px;
          cursor: pointer;
          padding: 6px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: background-color 0.2s;
        }
        .btn-settings:hover {
          background-color: #F5E6C8;
        }
        .btn-end {
          background-color: #E74C3C;
          color: #FFFFFF;
          border: none;
          padding: 8px 16px;
          border-radius: 20px;
          font-weight: 700;
          cursor: pointer;
          font-size: 16px;
          transition: background-color 0.2s;
        }
        .btn-end:hover {
          background-color: #C0392B;
        }

        .chat-area {
          flex-grow: 1;
          overflow-y: auto;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 20px;
          background-color: #FDF8F0;
        }
        .message-row {
          display: flex;
          width: 100%;
        }
        .message-row.ai {
          justify-content: flex-start;
        }
        .message-row.user {
          justify-content: flex-end;
        }
        .message-wrapper {
          display: flex;
          flex-direction: column;
          max-width: 80%;
        }
        .message-bubble {
          padding: 16px 20px;
          line-height: 1.5;
          box-shadow: 0 2px 8px rgba(0,0,0,0.04);
          position: relative;
          font-size: inherit;
        }
        .ai .message-bubble {
          background-color: #FFF3E0;
          border-radius: 0 20px 20px 20px;
          border: 1px solid #FFE0B2;
          color: #3D2E1F;
        }
        .ai-indicator {
          display: inline-block;
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background-color: #B8860B;
          margin-right: 8px;
        }
        .user .message-bubble {
          background-color: #F5F0E8;
          border-radius: 20px 0 20px 20px;
          border: 1px solid #E8DCC8;
          color: #3D2E1F;
        }
        .message-time {
          font-size: 12px;
          color: #8B7355;
          margin-top: 6px;
        }
        .ai .message-time {
          align-self: flex-start;
          margin-left: 4px;
        }
        .user .message-time {
          align-self: flex-end;
          margin-right: 4px;
        }

        .interim-speech-bar {
          background-color: #FFF9F2;
          border: 1px dashed #B8860B;
          padding: 10px 16px;
          margin: 0 20px;
          border-radius: 8px;
          font-size: 16px;
          color: #B8860B;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .quick-replies-container {
          padding: 14px 20px;
          background-color: rgba(253, 248, 240, 0.95);
          border-top: 1px solid #E8DCC8;
        }
        .quick-replies-title {
          font-size: 14px;
          font-weight: 700;
          color: #8B7355;
          margin-bottom: 10px;
        }
        .quick-replies-row {
          display: flex;
          gap: 10px;
          overflow-x: auto;
          padding-bottom: 6px;
          scrollbar-width: none;
        }
        .quick-replies-row::-webkit-scrollbar {
          display: none;
        }
        .chip-button {
          background-color: #FFFFFF;
          border: 1px solid #E8DCC8;
          color: #B8860B;
          padding: 10px 20px;
          border-radius: 24px;
          font-weight: 700;
          white-space: nowrap;
          cursor: pointer;
          transition: all 0.2s;
          font-size: inherit;
        }
        .chip-button:hover {
          border-color: #B8860B;
          background-color: #FFF9F0;
        }

        .bottom-controls {
          display: flex;
          flex-direction: column;
          background-color: #FFFFFF;
          border-top: 1px solid #E8DCC8;
          padding: 12px 20px 24px 20px;
          gap: 12px;
        }
        .input-row {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .text-input-wrapper {
          flex-grow: 1;
          display: flex;
          background-color: #FDF8F0;
          border: 1px solid #E8DCC8;
          border-radius: 24px;
          padding: 6px 16px;
          align-items: center;
        }
        .text-input {
          flex-grow: 1;
          background: transparent;
          border: none;
          outline: none;
          font-family: inherit;
          font-size: inherit;
          color: #3D2E1F;
          padding: 8px 0;
        }
        .text-input::placeholder {
          color: #A08A75;
        }
        .btn-send {
          background-color: #B8860B;
          border: none;
          color: white;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: background-color 0.2s;
        }
        .btn-send:hover {
          background-color: #8B6914;
        }
        .btn-send svg {
          width: 20px;
          height: 20px;
          fill: #FFFFFF;
        }

        .action-buttons {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0 10px;
        }
        .btn-action {
          background: transparent;
          border: none;
          cursor: pointer;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 4px;
          font-size: 14px;
          color: #8B7355;
          font-weight: 700;
        }
        .btn-action svg {
          width: 26px;
          height: 26px;
          fill: #8B7355;
        }
        .btn-action.active {
          color: #B8860B;
        }
        .btn-action.active svg {
          fill: #B8860B;
        }
        .btn-mic-main {
          width: 68px;
          height: 68px;
          border-radius: 50%;
          background-color: #B8860B;
          border: none;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 14px rgba(184, 134, 11, 0.45);
          cursor: pointer;
          transition: all 0.2s;
        }
        .btn-mic-main:hover {
          transform: scale(1.06);
        }
        .btn-mic-main.listening {
          background-color: #E74C3C;
          box-shadow: 0 0 20px rgba(231, 76, 60, 0.65);
          animation: listening-pulse 1.5s infinite;
        }
        @keyframes listening-pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.08); }
          100% { transform: scale(1); }
        }
        .btn-mic-main svg {
          width: 32px;
          height: 32px;
          fill: #FFFFFF;
        }

        /* Settings Sidebar */
        .settings-sidebar {
          position: absolute;
          top: 0;
          right: 0;
          width: 330px;
          height: 100%;
          background-color: #FFFFFF;
          box-shadow: -4px 0 20px rgba(0,0,0,0.08);
          z-index: 100;
          display: flex;
          flex-direction: column;
          transform: translateX(100%);
          transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .settings-sidebar.open {
          transform: translateX(0);
        }
        .settings-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px;
          border-bottom: 1px solid #E8DCC8;
        }
        .settings-title {
          font-size: 20px;
          font-weight: 700;
          margin: 0;
        }
        .btn-close-settings {
          background: transparent;
          border: none;
          font-size: 26px;
          cursor: pointer;
          color: #8B7355;
        }
        .settings-body {
          flex-grow: 1;
          overflow-y: auto;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 24px;
        }
        .settings-section {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .settings-label {
          font-weight: 700;
          font-size: 16px;
          color: #3D2E1F;
        }
        .toggle-group {
          display: flex;
          border: 1px solid #E8DCC8;
          border-radius: 10px;
          overflow: hidden;
          width: 100%;
        }
        .toggle-btn {
          flex: 1;
          background-color: #FFFFFF;
          border: none;
          padding: 12px;
          font-size: 14px;
          font-weight: 700;
          color: #8B7355;
          cursor: pointer;
          transition: all 0.2s;
        }
        .toggle-btn:not(:last-child) {
          border-right: 1px solid #E8DCC8;
        }
        .toggle-btn.active {
          background-color: #B8860B;
          color: #FFFFFF;
        }
        .voice-radio-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .voice-radio-option {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 10px 14px;
          border: 1px solid #E8DCC8;
          border-radius: 8px;
          cursor: pointer;
          font-size: 14px;
          font-weight: 500;
          transition: all 0.2s;
        }
        .voice-radio-option.active {
          border-color: #B8860B;
          background-color: #FFF9F0;
          font-weight: 700;
        }
        .voice-radio-option input {
          margin: 0;
          accent-color: #B8860B;
        }
        .settings-footer {
          padding: 20px;
          border-top: 1px solid #E8DCC8;
          background-color: #FDF8F0;
          font-size: 13px;
          color: #8B7355;
          line-height: 1.5;
        }
      `}</style>

      {/* Header Bar */}
      <header className="chat-header">
        <div className="header-info">
          <span className="header-emoji">📦</span>
          <div className="header-text">
            <h1 className="header-title">기억상자 AI</h1>
            <p className="header-subtitle">
              <span className="status-dot"></span>
              추억 이야기 중
            </p>
          </div>
        </div>
        <div className="header-actions">
          <button className="btn-settings" onClick={() => setIsSettingsOpen(true)} aria-label="설정 열기">
            ⚙️
          </button>
          <button className="btn-end" onClick={() => navigate('/summary')}>
            종료
          </button>
        </div>
      </header>

      {/* Settings Panel Sidebar */}
      <div className={`settings-sidebar ${isSettingsOpen ? 'open' : ''}`}>
        <div className="settings-header">
          <h2 className="settings-title">⚙️ 대화 설정</h2>
          <button className="btn-close-settings" onClick={() => setIsSettingsOpen(false)}>✕</button>
        </div>
        <div className="settings-body">
          {/* Font Size Settings */}
          <div className="settings-section">
            <span className="settings-label">글자 크기</span>
            <div className="toggle-group">
              <button
                className={`toggle-btn ${settings.fontSize === 'default' ? 'active' : ''}`}
                onClick={() => updateSettings({ fontSize: 'default' })}
              >
                기본
              </button>
              <button
                className={`toggle-btn ${settings.fontSize === 'large' ? 'active' : ''}`}
                onClick={() => updateSettings({ fontSize: 'large' })}
              >
                크게
              </button>
              <button
                className={`toggle-btn ${settings.fontSize === 'xlarge' ? 'active' : ''}`}
                onClick={() => updateSettings({ fontSize: 'xlarge' })}
              >
                매우 크게
              </button>
            </div>
          </div>

          {/* TTS Enable/Disable Settings */}
          <div className="settings-section">
            <span className="settings-label">AI 음성 읽기 (TTS)</span>
            <div className="toggle-group">
              <button
                className={`toggle-btn ${settings.ttsEnabled ? 'active' : ''}`}
                onClick={() => updateSettings({ ttsEnabled: true })}
              >
                켜기
              </button>
              <button
                className={`toggle-btn ${!settings.ttsEnabled ? 'active' : ''}`}
                onClick={() => updateSettings({ ttsEnabled: false })}
              >
                끄기
              </button>
            </div>
          </div>

          {/* TTS Voice Selection */}
          <div className="settings-section">
            <span className="settings-label">목소리 선택</span>
            <div className="voice-radio-group">
              {[
                { id: 'female1', label: '여성 목소리 1 (기본)' },
                { id: 'female2', label: '여성 목소리 2 (부드러움)' },
                { id: 'male1', label: '남성 목소리 1 (차분함)' },
                { id: 'male2', label: '남성 목소리 2 (따뜻함)' }
              ].map((v) => (
                <div
                  key={v.id}
                  className={`voice-radio-option ${settings.ttsVoice === v.id || (!settings.ttsVoice && v.id === 'female1') ? 'active' : ''}`}
                  onClick={() => updateSettings({ ttsVoice: v.id })}
                >
                  <input
                    type="radio"
                    name="ttsVoice"
                    checked={settings.ttsVoice === v.id || (!settings.ttsVoice && v.id === 'female1')}
                    readOnly
                  />
                  <span>{v.label}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Speaking Rate Settings */}
          <div className="settings-section">
            <span className="settings-label">말하기 속도</span>
            <div className="toggle-group">
              <button
                className={`toggle-btn ${settings.speechRate === 'slow' ? 'active' : ''}`}
                onClick={() => updateSettings({ speechRate: 'slow' })}
              >
                천천히
              </button>
              <button
                className={`toggle-btn ${settings.speechRate === 'normal' ? 'active' : ''}`}
                onClick={() => updateSettings({ speechRate: 'normal' })}
              >
                보통
              </button>
              <button
                className={`toggle-btn ${settings.speechRate === 'fast' ? 'active' : ''}`}
                onClick={() => updateSettings({ speechRate: 'fast' })}
              >
                빠르게
              </button>
            </div>
          </div>
        </div>
        <div className="settings-footer">
          * Web Speech API를 사용하여 브라우저에서 직접 한국어 음성을 합성하고 인식합니다. 인터넷 연결 상태나 OS 환경에 따라 지원되는 목소리가 다를 수 있습니다.
        </div>
      </div>

      {/* Chat Messages Area */}
      <main className="chat-area">
        {chatMessages.map((msg) => (
          <div key={msg.id} className={`message-row ${msg.role}`}>
            <div className="message-wrapper">
              <div className="message-bubble">
                {msg.role === 'ai' && <span className="ai-indicator"></span>}
                {msg.content}
              </div>
              <span className="message-time">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </main>

      {/* Interim Recognition Result (Only shown when speaking) */}
      {isListening && interimTranscript && (
        <div className="interim-speech-bar">
          <span>🎤 듣고 있어요:</span>
          <span>{interimTranscript}</span>
        </div>
      )}

      {/* Quick Reply Chips */}
      <div className="quick-replies-container">
        <p className="quick-replies-title">💡 이렇게 말씀해 보세요</p>
        <div className="quick-replies-row">
          {getQuickReplies().map((replyText, i) => (
            <button
              key={i}
              className="chip-button"
              onClick={() => {
                if (replyText === "대화 종료하고 요약 보기") {
                  navigate('/summary');
                } else {
                  handleUserResponse(replyText);
                }
              }}
            >
              {replyText}
            </button>
          ))}
        </div>
      </div>

      {/* Bottom Bar Controls */}
      <footer className="bottom-controls">
        <div className="input-row">
          <div className="text-input-wrapper">
            <input
              ref={inputRef}
              type="text"
              className="text-input"
              placeholder="직접 입력해 주세요..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleUserResponse(inputValue);
                }
              }}
            />
            {inputValue.trim() && (
              <button className="btn-send" onClick={() => handleUserResponse(inputValue)} aria-label="전송">
                <svg viewBox="0 0 24 24">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                </svg>
              </button>
            )}
          </div>
        </div>

        <div className="action-buttons">
          <button
            className={`btn-action ${inputValue ? 'active' : ''}`}
            onClick={() => inputRef.current?.focus()}
          >
            <svg viewBox="0 0 24 24">
              <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z" />
            </svg>
            글자 입력
          </button>

          <button
            className={`btn-mic-main ${isListening ? 'listening' : ''}`}
            onClick={toggleMic}
            aria-label="말하기"
          >
            <svg viewBox="0 0 24 24">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z" />
            </svg>
          </button>

          <button className="btn-action" onClick={() => navigate('/summary')}>
            <svg viewBox="0 0 24 24">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10H7v-2h10v2zm0-4H7V7h10v2zm0 8H7v-2h10v2z" />
            </svg>
            대화 종료
          </button>
        </div>
      </footer>
    </div>
  );
};

export default ChatPage;
