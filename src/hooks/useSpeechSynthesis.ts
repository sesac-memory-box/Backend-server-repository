import { useState, useEffect, useCallback, useRef } from 'react';

export interface SpeakOptions {
  voiceURI?: string;
  rate?: number; // Supports speed: 0.7, 1.0, 1.3 etc.
  pitch?: number;
}

export const useSpeechSynthesis = () => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  const loadVoices = useCallback(() => {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      setVoices(window.speechSynthesis.getVoices());
    }
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined' || !window.speechSynthesis) {
      console.warn('SpeechSynthesis is not supported in this browser.');
      return;
    }

    loadVoices();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }

    const checkSpeakingInterval = setInterval(() => {
      if (window.speechSynthesis) {
        setIsSpeaking(window.speechSynthesis.speaking);
      }
    }, 200);

    return () => {
      clearInterval(checkSpeakingInterval);
    };
  }, [loadVoices]);

  const getKoreanVoices = useCallback(() => {
    return voices.filter((voice) => voice.lang.includes('ko') || voice.lang.includes('KO'));
  }, [voices]);

  const speak = useCallback(
    (text: string, options: SpeakOptions = {}) => {
      if (typeof window === 'undefined' || !window.speechSynthesis) {
        console.warn('SpeechSynthesis is not supported in this browser.');
        return;
      }

      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utteranceRef.current = utterance;

      if (options.voiceURI) {
        const foundVoice = voices.find((v) => v.voiceURI === options.voiceURI);
        if (foundVoice) {
          utterance.voice = foundVoice;
        }
      } else {
        const koVoices = voices.filter((voice) => voice.lang.includes('ko') || voice.lang.includes('KO'));
        if (koVoices.length > 0) {
          utterance.voice = koVoices[0];
        }
      }

      utterance.rate = options.rate !== undefined ? options.rate : 1.0;
      utterance.pitch = options.pitch !== undefined ? options.pitch : 1.0;

      utterance.onstart = () => {
        setIsSpeaking(true);
      };

      utterance.onend = () => {
        setIsSpeaking(false);
      };

      utterance.onerror = (e) => {
        console.error('SpeechSynthesis error:', e);
        setIsSpeaking(false);
      };

      window.speechSynthesis.speak(utterance);
    },
    [voices]
  );

  const cancel = useCallback(() => {
    if (typeof window === 'undefined' || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  }, []);

  return {
    speak,
    cancel,
    isSpeaking,
    voices,
    getKoreanVoices,
    isSupported: typeof window !== 'undefined' && !!window.speechSynthesis,
  };
};
