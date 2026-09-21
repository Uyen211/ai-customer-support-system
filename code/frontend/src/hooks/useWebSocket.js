import { useState, useEffect, useRef, useCallback } from 'react';
import { useAuth } from './useAuth';

export function useWebSocket(url, options = {}) {
  const { autoReconnect = true } = options;
  const { token } = useAuth();
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const ws = useRef(null);
  const reconnectTimer = useRef(null);

  useEffect(() => {
    if (!url || !token) return;
    let cancelled = false;
    let retry = 0;

    const connect = () => {
      if (cancelled) return;
      const wsUrl = `${url}${url.includes('?') ? '&' : '?'}token=${encodeURIComponent(token)}`;
      const socket = new WebSocket(wsUrl);
      ws.current = socket;

      socket.onopen = () => {
        retry = 0;
        setIsConnected(true);
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setLastMessage(data);
          setMessages((prev) => [...prev, data]);
        } catch (err) {
          console.error('Failed to parse websocket message', err);
        }
      };

      socket.onclose = () => {
        setIsConnected(false);
        if (cancelled) return;
        if (autoReconnect) {
          retry += 1;
          reconnectTimer.current = setTimeout(connect, Math.min(retry * 2000, 10000));
        }
      };

      socket.onerror = () => {
        try { socket.close(); } catch (err) { /* noop */ }
      };
    };

    connect();

    return () => {
      cancelled = true;
      if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
      if (ws.current) {
        ws.current.onopen = null;
        ws.current.onmessage = null;
        ws.current.onclose = null;
        ws.current.onerror = null;
        ws.current.close();
        ws.current = null;
      }
    };
  }, [url, token, autoReconnect]);

  // Gửi dữ liệu JSON qua WebSocket (trả true nếu gửi thành công)
  const send = useCallback((data) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(typeof data === 'string' ? data : JSON.stringify(data));
      return true;
    }
    return false;
  }, []);

  // Provide a way to consume messages
  const popMessage = useCallback(() => {
    if (messages.length === 0) return null;
    const msg = messages[0];
    setMessages((prev) => prev.slice(1));
    return msg;
  }, [messages]);

  return { isConnected, popMessage, messages, lastMessage, send };
}