import React, { useState } from 'react';
import { Bot, User, FileText, Sparkles } from 'lucide-react';
import { formatTimeAgo } from '../../utils/formatters';
import { CitationsDrawer } from './CitationsDrawer';

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
            <div className="whitespace-pre-wrap break-words">
              {message.content}
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
