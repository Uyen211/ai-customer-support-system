import React, { useEffect, useRef } from 'react';
import { MessageItem } from './MessageItem';
import { LoadingSpinner } from '../common/LoadingSpinner';

export function MessageList({
  messages = [],
  isStreaming = false,
  streamedContent = '',
  hasMore = false,
  isLoadingMore = false,
  onLoadMore,
}) {
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);

  const scrollToBottom = (smooth = true) => {
    messagesEndRef.current?.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto' });
  };

  useEffect(() => {
    scrollToBottom(true);
  }, [messages, streamedContent, isStreaming]);

  const handleScroll = () => {
    if (!containerRef.current || isLoadingMore || !hasMore) return;
    if (containerRef.current.scrollTop === 0) {
      if (onLoadMore) onLoadMore();
    }
  };

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className="flex-1 overflow-y-auto px-4 sm:px-6 py-4 space-y-2 scroll-smooth"
    >
      {/* Lazy loading top button */}
      {hasMore && (
        <div className="text-center py-2">
          <button
            onClick={onLoadMore}
            disabled={isLoadingMore}
            className="px-4 py-1.5 rounded-full bg-[#EFE7D3] hover:bg-[#95BBEA] text-[#2B2523] text-xs font-medium transition-colors disabled:opacity-50"
          >
            {isLoadingMore ? 'Đang tải tin nhắn cũ...' : 'Tải 50 tin nhắn cũ hơn'}
          </button>
        </div>
      )}

      {/* Messages */}
      {messages.map((msg, idx) => (
        <MessageItem key={msg.id || idx} message={msg} />
      ))}

      {/* Streaming response active item */}
      {isStreaming && streamedContent && (
        <MessageItem
          message={{
            sender_type: 'BOT',
            content: streamedContent,
            created_at: new Date().toISOString(),
          }}
          isStreaming={true}
        />
      )}

      {/* Invisible marker for auto-scroll */}
      <div ref={messagesEndRef} />
    </div>
  );
}
