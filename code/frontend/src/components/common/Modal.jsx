import React, { useEffect } from 'react';
import { X } from 'lucide-react';

export function Modal({ isOpen, onClose, title, children, className = '' }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#2B2523]/40 backdrop-blur-sm animate-fade-in">
      <div
        className={`relative w-full max-w-lg bg-[#FFF8E7] rounded-3xl p-6 sm:p-8 shadow-diffused-lg border border-[#EFE7D3] ${className}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between pb-4 mb-4 border-b border-[#EFE7D3]">
          {title && <h3 className="font-serif-editorial text-2xl text-[#2B2523]">{title}</h3>}
          <button
            onClick={onClose}
            className="p-2 text-[#2B2523]/60 hover:text-[#930500] hover:bg-[#EFE7D3] rounded-full transition-colors duration-200"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
}
