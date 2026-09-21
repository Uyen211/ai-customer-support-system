import { useState, useCallback, useRef } from 'react';
import { API_BASE_URL } from '../utils/constants';

export function useSSEChat() {
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamedContent, setStreamedContent] = useState('');
  const [citations, setCitations] = useState([]);
  const [error, setError] = useState(null);
  const abortControllerRef = useRef(null);

  const sendMessage = useCallback(
    async ({ conversationId, message, onToken, onComplete, onError, onNotice }) => {
      setIsStreaming(true);
      setStreamedContent('');
      setCitations([]);
      setError(null);

      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      abortControllerRef.current = new AbortController();

      try {
        const token = sessionStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/chat/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
          body: JSON.stringify({
            conversation_id: conversationId,
            message: message,
          }),
          signal: abortControllerRef.current.signal,
        });

        if (!response.ok) {
          const errJson = await response.json().catch(() => ({}));
          throw new Error(errJson.detail || errJson.message || `Lỗi máy chủ (${response.status})`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';
        let currentText = '';
        let finalCitations = [];

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const events = buffer.split('\n\n');
          buffer = events.pop() || ''; // Keep last incomplete chunk in buffer

          for (const rawEvent of events) {
            if (!rawEvent.trim()) continue;

            const lines = rawEvent.split('\n');
            let eventType = 'message';
            let dataStr = '';

            for (const line of lines) {
              if (line.startsWith('event: ')) {
                eventType = line.slice(7).trim();
              } else if (line.startsWith('data: ')) {
                dataStr += line.slice(6);
              }
            }

            if (!dataStr) continue;

            try {
              const dataObj = JSON.parse(dataStr);

              if (eventType === 'token') {
                const tokenText = dataObj.token || '';
                currentText += tokenText;
                setStreamedContent(currentText);
                if (onToken) onToken(tokenText, currentText);
              } else if (eventType === 'done') {
                finalCitations = dataObj.citations || [];
                setCitations(finalCitations);
                if (onComplete) {
                  onComplete({
                    fullText: dataObj.full_text || currentText,
                    citations: finalCitations,
                    standaloneQuery: dataObj.standalone_query,
                  });
                }
              } else if (eventType === 'notice') {
                if (onNotice) onNotice(dataObj.message);
              } else if (eventType === 'error') {
                const errText = dataObj.error || 'Có lỗi xảy ra.';
                setError(errText);
                if (onError) onError(errText);
              }
            } catch (err) {
              console.warn('Lỗi parse SSE JSON:', err, dataStr);
            }
          }
        }
      } catch (err) {
        if (err.name === 'AbortError') return;
        const errMessage = err.message || 'Không thể kết nối đến máy chủ stream.';
        setError(errMessage);
        if (onError) onError(errMessage);
      } finally {
        setIsStreaming(false);
      }
    },
    []
  );

  const stopStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsStreaming(false);
    }
  }, []);

  return {
    isStreaming,
    streamedContent,
    citations,
    error,
    sendMessage,
    stopStream,
  };
}
