import React, { useState } from 'react';
import { Modal } from '../common/Modal';
import { FileText, Bookmark, ChevronDown, ChevronUp, BookOpen } from 'lucide-react';

export function CitationsDrawer({ isOpen, onClose, citations = [] }) {
  const [expandedIndices, setExpandedIndices] = useState({});

  const toggleExpand = (idx) => {
    setExpandedIndices((prev) => ({
      ...prev,
      [idx]: !prev[idx],
    }));
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="📌 Trích Dẫn Nguồn Tài Liệu (RAG)"
      className="max-w-2xl"
    >
      <div className="space-y-4 max-h-[65vh] overflow-y-auto pr-1">
        {citations.length === 0 ? (
          <p className="text-sm text-[#2B2523]/60 italic text-center py-6">
            Không tìm thấy thông tin trích dẫn cho câu trả lời này.
          </p>
        ) : (
          citations.map((cite, idx) => {
            const docName = cite.document_name || cite.source_document || cite.title || 'Tài liệu PetHome';
            const section = cite.section_title || (cite.metadata && (cite.metadata.section || cite.metadata.title));
            const page = cite.page_number || (cite.metadata && cite.metadata.page_number);
            const snippet = cite.content_snippet || cite.snippet_text || cite.content || cite.text || '';
            const parentContent = cite.parent_content || (cite.metadata && cite.metadata.parent_content) || snippet;
            const isExpanded = !!expandedIndices[idx];

            return (
              <div
                key={idx}
                className="bg-[#FFF8E7] rounded-2xl p-4 border border-[#EFE7D3] shadow-diffused-sm space-y-2 hover:border-[#95BBEA] transition-colors"
              >
                {/* Document Header */}
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-[#930500] flex items-center gap-1.5 truncate max-w-[80%]">
                    <FileText className="w-4 h-4 text-[#930500] shrink-0" />
                    <span>{docName}</span>
                  </span>
                  {page && (
                    <span className="bg-[#95BBEA]/30 text-[#2B2523] px-2 py-0.5 rounded-full text-[11px] font-medium shrink-0">
                      Trang {page}
                    </span>
                  )}
                </div>

                {/* Section Title */}
                {section && (
                  <div className="text-xs font-semibold text-[#2B2523] flex items-center gap-1">
                    <Bookmark className="w-3.5 h-3.5 text-[#95BBEA] shrink-0" />
                    <span>{section}</span>
                  </div>
                )}

                {/* Snippet / Preview Content */}
                <div className="text-xs text-[#2B2523]/90 leading-relaxed bg-white/70 p-3 rounded-xl border border-[#EFE7D3]">
                  <p className="font-light italic text-[#2B2523]/80">
                    "{isExpanded ? parentContent : snippet}"
                  </p>
                </div>

                {/* Expand / Collapse Button for parent_content */}
                {parentContent && parentContent !== snippet && (
                  <div className="pt-1 flex justify-end">
                    <button
                      onClick={() => toggleExpand(idx)}
                      className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#930500] hover:text-[#2B2523] bg-[#930500]/10 hover:bg-[#930500]/20 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
                    >
                      <BookOpen className="w-3 h-3" />
                      <span>{isExpanded ? 'Thu gọn nội dung' : 'Mở rộng nội dung đầy đủ'}</span>
                      {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    </button>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      <div className="mt-6 pt-4 border-t border-[#EFE7D3] text-right">
        <button
          onClick={onClose}
          className="px-5 py-2 rounded-full bg-[#EFE7D3] text-[#2B2523] text-xs font-semibold hover:bg-[#95BBEA] transition-colors cursor-pointer"
        >
          Đóng cửa sổ
        </button>
      </div>
    </Modal>
  );
}
