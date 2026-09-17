import React from 'react';

export function Badge({ children, variant = 'bot', className = '' }) {
  const variantStyles = {
    bot: 'bg-[#95BBEA] text-[#1F242B] border border-[#95BBEA]/30',
    waiting_human: 'bg-[#FEF3C7] text-[#92400E] border border-[#FDE68A]',
    human: 'bg-[#D1FAE5] text-[#065F46] border border-[#A7F3D0]',
    closed: 'bg-[#EFE7D3] text-[#78716C] border border-[#EFE7D3]',
    primary: 'bg-[#930500] text-[#FFF8E7]',
    outline: 'border border-[#EFE7D3] text-[#2B2523]',
  };

  const key = String(variant).toLowerCase();
  const selectedStyle = variantStyles[key] || variantStyles.bot;

  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider ${selectedStyle} ${className}`}
    >
      {children}
    </span>
  );
}
