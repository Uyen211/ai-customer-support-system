import React, { useState } from 'react';
import { Send, Square, AlertCircle, CheckCircle2, Lock, Clock, UserCheck, Bot } from 'lucide-react';
import { MessageList } from './MessageList';
import { SuggestionButtons } from './SuggestionButtons';
import { Badge } from '../common/Badge';
import { Button } from '../common/Button';

export function ChatWindow({
  conversation,
  messages = [],
  isStreaming = false,
  streamedContent = '',
  hasMore = false,
  isLoadingMore = false,
  onLoadMore,
  onSendMessage,
  onStopStream,
  onCloseConversation,
}) {
  const [inputText, setInputText] = useState('');

  const mode = conversation?.mode || 'BOT';
  const isClosed = mode === 'CLOSED';
  const isWaitingHuman = mode === 'WAITING_HUMAN';

  const handleSend = (e) => {
    e?.preventDefault();
    if (!inputText.trim() || isStreaming || isClosed) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  const handleSelectSuggestion = (promptText) => {
    if (isClosed) return;
    onSendMessage(promptText);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-[#FFF8E7] rounded-3xl border border-[#EFE7D3] shadow-editorial overflow-hidden">
      
      {/* 1. Header Bar */}
      <div className="px-6 py-4 border-b border-[#EFE7D3] bg-[#FFF8E7] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-[#95BBEA] text-[#1F242B] flex items-center justify-center font-bold text-sm">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-serif-editorial text-lg font-bold text-[#2B2523] flex items-center gap-2">
              Trợ Lý AI PetHome 24/7
            </h3>
            <div className="flex items-center gap-2 mt-0.5">
              <Badge variant={mode}>{mode}</Badge>
              <span className="text-[11px] text-[#2B2523]/50">
                Phiên #{conversation?.id ? String(conversation.id).slice(0, 8) : 'Mới'}
              </span>
            </div>
          </div>
        </div>

        {/* Action Button: End Conversation */}
        {!isClosed && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onCloseConversation}
            className="text-xs text-[#930500] hover:bg-[#930500]/10"
          >
            Đóng Phiên Hỗ Trợ
          </Button>
        )}
      </div>

      {/* 2. Mode Warning Banners */}
      {isWaitingHuman && (
        <div className="px-6 py-2.5 bg-[#FEF3C7] border-b border-[#FDE68A] text-xs text-[#92400E] flex items-center gap-2 animate-fade-in font-medium">
          <Clock className="w-4 h-4 text-[#D97706] shrink-0" />
          <span>Cuộc trò chuyện đang được chuyển tiếp tới nhân viên tư vấn. Vui lòng chờ trong giây lát...</span>
        </div>
      )}

      {isClosed && (
        <div className="px-6 py-2.5 bg-[#EFE7D3] border-b border-[#EFE7D3] text-xs text-[#78716C] flex items-center gap-2 animate-fade-in font-medium">
          <Lock className="w-4 h-4 shrink-0" />
          <span>Phiên trò chuyện này đã kết thúc. Ô nhập liệu đã bị khóa. Bạn có thể bấm "Bắt đầu cuộc trò chuyện mới" để tiếp tục.</span>
        </div>
      )}

      {/* 3. Messages List Area */}
      <MessageList
        messages={messages}
        isStreaming={isStreaming}
        streamedContent={streamedContent}
        hasMore={hasMore}
        isLoadingMore={isLoadingMore}
        onLoadMore={onLoadMore}
      />

      {/* 4. Suggestion Buttons (when list is short or just started) */}
      {messages.length <= 2 && !isClosed && (
        <div className="px-6 pb-2">
          <SuggestionButtons onSelectSuggestion={handleSelectSuggestion} />
        </div>
      )}

      {/* 5. Input Bar */}
      <div className="p-4 sm:p-6 border-t border-[#EFE7D3] bg-[#FFF8E7]">
        <form onSubmit={handleSend} className="relative flex items-center gap-2">
          <textarea
            rows={1}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isClosed || isStreaming}
            placeholder={
              isClosed
                ? 'Phiên chat đã đóng...'
                : 'Nhập câu hỏi cho Trợ lý AI (Ví dụ: Giá hạt Nutrience, chính sách đổi trả...)'
            }
            className="w-full bg-[#FFF8E7] text-[#2B2523] placeholder-[#2B2523]/40 border border-[#EFE7D3] focus:border-[#930500] rounded-2xl py-3 pl-4 pr-14 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-[#930500]/20 disabled:bg-[#EFE7D3]/50 disabled:cursor-not-allowed transition-all"
          />

          <div className="absolute right-3">
            {isStreaming ? (
              <button
                type="button"
                onClick={onStopStream}
                className="w-9 h-9 rounded-full bg-[#930500] text-[#FFF8E7] flex items-center justify-center hover:bg-[#7a0400] transition-colors cursor-pointer"
                title="Dừng stream"
              >
                <Square className="w-4 h-4 fill-current" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={!inputText.trim() || isClosed}
                className="w-9 h-9 rounded-full bg-[#930500] text-[#FFF8E7] flex items-center justify-center hover:bg-[#7a0400] disabled:opacity-40 disabled:pointer-events-none transition-all cursor-pointer shadow-diffused-sm"
              >
                <Send className="w-4 h-4" />
              </button>
            )}
          </div>
        </form>
        <p className="text-[11px] text-[#2B2523]/50 mt-2 text-center">
          Nhấn Enter để gửi, Shift + Enter để xuống dòng. Trợ lý AI phản hồi tức thì với trích dẫn RAG.
        </p>
      </div>

    </div>
  );
}
