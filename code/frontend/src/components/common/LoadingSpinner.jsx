import React from 'react';

export function LoadingSpinner({ size = 'md', className = '', label = 'Đang tải...' }) {
  const sizeMap = {
    sm: 'w-5 h-5 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
  };

  return (
    <div className={`flex flex-col items-center justify-center p-4 gap-3 ${className}`}>
      <div
        className={`${sizeMap[size]} border-[#95BBEA] border-t-[#930500] rounded-full animate-spin`}
      />
      {label && <span className="text-xs text-[#2B2523]/70 font-medium">{label}</span>}
    </div>
  );
}
