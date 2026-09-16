import React from 'react';
import { Modal } from '../common/Modal';
import { FileText, Bookmark, ExternalLink } from 'lucide-react';

export function CitationsDrawer({ isOpen, onClose, citations = [] }) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="📌 Trích Dẫn Nguồn Tài Liệu (RAG)"
      className="max-w-2xl"
    >
      <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-1">
        {citations.length === 0 ? (
          <p className="text-sm text-[#2B2523]/60 italic text-center py-6">
            Không tìm thấy thông tin trích dẫn cho câu trả lời này.
          </p>
        ) : (
          citations.map((cite, idx) => (
            <div
              key={idx}
              className="bg-[#FFF8E7] rounded-2xl p-4 border border-[#EFE7D3] shadow-diffused-sm space-y-2 hover:border-[#95BBEA] transition-colors"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-[#930500] flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-[#930500]" />
                  {cite.source_document || cite.title || 'Tài liệu PetHome'}
                </span>
                {cite.page_number && (
                  <span className="bg-[#95BBEA]/30 text-[#2B2523] px-2 py-0.5 rounded-full text-[11px] font-medium">
                    Trang {cite.page_number}
                  </span>
                )}
              </div>

              {cite.section_title && (
                <div className="text-xs font-semibold text-[#2B2523] flex items-center gap-1">
                  <Bookmark className="w-3.5 h-3.5 text-[#95BBEA]" />
                  {cite.section_title}
                </div>
              )}

              <p className="text-xs text-[#2B2523]/80 leading-relaxed font-light italic bg-white/60 p-3 rounded-xl border border-[#EFE7D3]/60">
                "{cite.snippet_text || cite.content || cite.text}"
              </p>
            </div>
          ))
        )}
      </div>

      <div className="mt-6 pt-4 border-t border-[#EFE7D3] text-right">
        <button
          onClick={onClose}
          className="px-5 py-2 rounded-full bg-[#EFE7D3] text-[#2B2523] text-xs font-semibold hover:bg-[#95BBEA] transition-colors"
        >
          Đóng cửa sổ
        </button>
      </div>
    </Modal>
  );
}
