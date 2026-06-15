import React, { createContext, useContext, useState } from 'react';

export interface GuardianInfo {
  hometown: string;
  pastJob: string;
  favoriteFood: string;
  memoryPlace: string;
  favoriteSong: string;
  sensitiveTopics: string;
}

export interface ChatMessage {
  id: string;
  role: 'ai' | 'user';
  content: string;
  timestamp: Date;
}

export interface Settings {
  fontSize: 'default' | 'large' | 'xlarge';
  ttsEnabled: boolean;
  ttsVoice: string;
  speechRate: 'slow' | 'normal' | 'fast';
}

export interface AppState {
  guardianInfo: GuardianInfo;
  chatMessages: ChatMessage[];
  settings: Settings;
  setGuardianInfo: (info: GuardianInfo) => void;
  addMessage: (msg: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
  clearMessages: () => void;
  updateSettings: (settings: Partial<Settings>) => void;
}

const defaultGuardianInfo: GuardianInfo = {
  hometown: '',
  pastJob: '',
  favoriteFood: '',
  memoryPlace: '',
  favoriteSong: '',
  sensitiveTopics: '',
};

const defaultSettings: Settings = {
  fontSize: 'large', // default large for senior friendliness
  ttsEnabled: true,
  ttsVoice: '',
  speechRate: 'normal',
};

const AppContext = createContext<AppState | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [guardianInfo, setGuardianInfoState] = useState<GuardianInfo>(() => {
    try {
      const saved = localStorage.getItem('guardianInfo');
      return saved ? JSON.parse(saved) : defaultGuardianInfo;
    } catch {
      return defaultGuardianInfo;
    }
  });

  const [chatMessages, setChatMessagesState] = useState<ChatMessage[]>(() => {
    try {
      const saved = localStorage.getItem('chatMessages');
      if (saved) {
        const parsed = JSON.parse(saved);
        return parsed.map((m: any) => ({ ...m, timestamp: new Date(m.timestamp) }));
      }
      return [];
    } catch {
      return [];
    }
  });

  const [settings, setSettings] = useState<Settings>(() => {
    try {
      const saved = localStorage.getItem('settings');
      return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
    } catch {
      return defaultSettings;
    }
  });

  const setGuardianInfo = (info: GuardianInfo) => {
    setGuardianInfoState(info);
    localStorage.setItem('guardianInfo', JSON.stringify(info));
  };

  const addMessage = (msg: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    const newMessage: ChatMessage = {
      ...msg,
      id: Math.random().toString(36).substring(2, 9),
      timestamp: new Date(),
    };
    setChatMessagesState((prev) => {
      const updated = [...prev, newMessage];
      localStorage.setItem('chatMessages', JSON.stringify(updated));
      return updated;
    });
  };

  const clearMessages = () => {
    setChatMessagesState([]);
    localStorage.removeItem('chatMessages');
  };

  const updateSettings = (newSettings: Partial<Settings>) => {
    setSettings((prev) => {
      const updated = { ...prev, ...newSettings };
      localStorage.setItem('settings', JSON.stringify(updated));
      return updated;
    });
  };

  return (
    <AppContext.Provider
      value={{
        guardianInfo,
        chatMessages,
        settings,
        setGuardianInfo,
        addMessage,
        clearMessages,
        updateSettings,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppStore = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppStore must be used within an AppProvider');
  }
  return context;
};
