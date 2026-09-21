import { useState, useEffect, useRef } from 'react';
import { useAuth } from './useAuth';

export function useWebSocket(url) {
  const { token } = useAuth();
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    if (!token) return;

    // Phụ thuộc vào môi trường, ghép token vào protocol hoặc query
    const wsUrl = `${url}?token=${token}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      setIsConnected(true);
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]);
      } catch (err) {
        console.error("Failed to parse websocket message", err);
      }
    };

    ws.current.onclose = () => {
      setIsConnected(false);
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [url, token]);

  // Provide a way to consume messages
  const popMessage = () => {
    if (messages.length === 0) return null;
    const msg = messages[0];
    setMessages((prev) => prev.slice(1));
    return msg;
  };

  return { isConnected, popMessage, messages };
}
