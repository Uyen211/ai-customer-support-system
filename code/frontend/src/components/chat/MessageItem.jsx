import React, { useState } from 'react';
import { Bot, User, FileText } from 'lucide-react';
import { formatTimeAgo } from '../../utils/formatters';
import { CitationsDrawer } from './CitationsDrawer';

// Helper format inline Markdown: **bold**, *italic*, `code`
function formatInlineText(text, isCustomer) {
  if (!text) return '';
  // Match **bold**, *italic*, `code`
  const regex = /(\*\*.*?\*\*|\*.*?\*|`.*?`)/g;
  const parts = text.split(regex);

  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
      const inner = part.slice(2, -2);
      return (
        <strong
          key={index}
          className={`font-bold ${isCustomer ? 'text-white underline decoration-white/40' : 'text-[#930500]'}`}
        >
          {inner}
        </strong>
      );
    }
    if (part.startsWith('*') && part.endsWith('*') && part.length > 2) {
      const inner = part.slice(1, -1);
      return (
        <strong
          key={index}
          className={`font-semibold ${isCustomer ? 'text-white' : 'text-[#930500]'}`}
        >
          {inner}
        </strong>
      );
    }
    if (part.startsWith('`') && part.endsWith('`') && part.length > 2) {
      const inner = part.slice(1, -1);
      return (
        <code
          key={index}
          className={`px-1.5 py-0.5 rounded text-xs font-mono ${
            isCustomer ? 'bg-white/20 text-white' : 'bg-[#EFE7D3] text-[#930500]'
          }`}
        >
          {inner}
        </code>
      );
    }
    return part;
  });
}

// Helper render Markdown blocks
function renderMarkdownContent(content, isCustomer) {
  if (!content) return null;
  const lines = content.split('\n');

  return lines.map((line, idx) => {
    const trimmed = line.trim();

    if (trimmed.startsWith('### ')) {
      return (
        <h4 key={idx} className="font-serif-editorial text-base font-bold my-2 text-[#2B2523]">
          {formatInlineText(trimmed.slice(4), isCustomer)}
        </h4>
      );
    }
    if (trimmed.startsWith('## ')) {
      return (
        <h3 key={idx} className="font-serif-editorial text-lg font-bold my-2 text-[#2B2523]">
          {formatInlineText(trimmed.slice(3), isCustomer)}
        </h3>
      );
    }
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      return (
        <div key={idx} className="flex items-start gap-2 my-1 pl-2">
          <span className={`w-1.5 h-1.5 rounded-full mt-2 shrink-0 ${isCustomer ? 'bg-white' : 'bg-[#930500]'}`} />
          <span>{formatInlineText(trimmed.slice(2), isCustomer)}</span>
        </div>
      );
    }
    if (/^\d+\.\s/.test(trimmed)) {
      const numMatch = trimmed.match(/^(\d+)\.\s/);
      const num = numMatch ? numMatch[1] : '';
      const rest = trimmed.replace(/^\d+\.\s/, '');
      return (
        <div key={idx} className="flex items-start gap-1.5 my-1 pl-2">
          <span className={`font-bold text-xs mt-0.5 shrink-0 ${isCustomer ? 'text-white' : 'text-[#930500]'}`}>
            {num}.
          </span>
          <span>{formatInlineText(rest, isCustomer)}</span>
        </div>
      );
    }
    if (!trimmed) {
      return <div key={idx} className="h-2" />;
    }

    return <div key={idx} className="my-0.5">{formatInlineText(line, isCustomer)}</div>;
  });
}

export function MessageItem({ message, isStreaming = false }) {
  const [isCitationsOpen, setIsCitationsOpen] = useState(false);
  const isCustomer = message.sender_type === 'CUSTOMER';
  const hasCitations = message.citations && message.citations.length > 0;

  return (
    <>
      <div className={`flex gap-3 my-4 animate-fade-in ${isCustomer ? 'flex-row-reverse' : 'flex-row'}`}>
        
        {/* Avatar */}
        <div
          className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0 text-xs font-bold shadow-diffused-sm ${
            isCustomer
              ? 'bg-[#930500] text-[#FFF8E7]'
              : 'bg-[#95BBEA] text-[#1F242B]'
          }`}
        >
          {isCustomer ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
        </div>

        {/* Message Content Bubble */}
        <div className={`max-w-[85%] sm:max-w-[75%] flex flex-col ${isCustomer ? 'items-end' : 'items-start'}`}>
          
          {/* Header info */}
          <div className="flex items-center gap-2 mb-1 px-1">
            <span className="text-[11px] font-semibold text-[#2B2523]/70">
              {isCustomer ? 'Bạn' : message.sender_type === 'BOT' ? 'Trợ lý AI PetHome' : 'Tư vấn viên'}
            </span>
            {message.created_at && (
              <span className="text-[10px] text-[#2B2523]/50">
                {formatTimeAgo(message.created_at)}
              </span>
            )}
          </div>

          {/* Bubble body */}
          <div
            className={`p-4 rounded-3xl text-sm leading-relaxed ${
              isCustomer
                ? 'bg-[#930500] text-[#FFF8E7] rounded-tr-none shadow-diffused-sm'
                : 'bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] rounded-tl-none shadow-editorial'
            }`}
          >
            <div className="break-words">
              {renderMarkdownContent(message.content, isCustomer)}
              {isStreaming && (
                <span className="inline-block w-2 h-4 ml-1 bg-[#930500] animate-pulse rounded-full align-middle" />
              )}
            </div>

            {/* Citations trigger button */}
            {hasCitations && !isCustomer && (
              <div className="mt-3 pt-3 border-t border-[#EFE7D3] flex items-center justify-between">
                <button
                  onClick={() => setIsCitationsOpen(true)}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#95BBEA]/30 hover:bg-[#95BBEA] text-[#2B2523] text-xs font-medium transition-colors cursor-pointer"
                >
                  <FileText className="w-3.5 h-3.5 text-[#930500]" />
                  <span>Trích dẫn ({message.citations.length} nguồn)</span>
                </button>
              </div>
            )}
          </div>

        </div>

      </div>

      {/* Citations Modal Drawer */}
      {hasCitations && (
        <CitationsDrawer
          isOpen={isCitationsOpen}
          onClose={() => setIsCitationsOpen(false)}
          citations={message.citations}
        />
      )}
    </>
  );
}
