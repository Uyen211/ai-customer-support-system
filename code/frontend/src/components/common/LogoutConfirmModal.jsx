import React from 'react';

export function LogoutConfirmModal({ isOpen, onClose, onConfirm, title, message }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#2B2523]/60 backdrop-blur-sm animate-fade-in">
      <div 
        className="relative w-full max-w-md bg-[#FFF8E7] rounded-2xl p-6 shadow-2xl border border-[#930500]/20 transform transition-all animate-scale-up"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header Icon */}
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-[#930500]/10 text-[#930500] mb-4">
          <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </div>

        {/* Content */}
        <div className="text-center">
          <h3 className="text-xl font-bold text-[#2B2523] mb-2 font-serif-editorial">
            {title || "Xác nhận đăng xuất"}
          </h3>
          <p className="text-sm text-[#2B2523]/70 mb-6 leading-relaxed">
            {message || "Bạn có chắc chắn muốn đăng xuất khỏi hệ thống Trợ lý CSKH PetHome không?"}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-end space-x-3 pt-2 border-t border-[#930500]/10">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 px-4 py-2.5 rounded-xl border border-[#2B2523]/20 text-[#2B2523] text-sm font-medium hover:bg-[#2B2523]/5 transition-colors"
          >
            Hủy bỏ
          </button>
          <button
            type="button"
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className="flex-1 px-4 py-2.5 rounded-xl bg-[#930500] hover:bg-[#7a0400] text-white text-sm font-medium shadow-md hover:shadow-lg transition-all"
          >
            Đăng xuất
          </button>
        </div>
      </div>
    </div>
  );
}
