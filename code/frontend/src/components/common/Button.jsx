import React from 'react';
import { Loader2 } from 'lucide-react';

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled = false,
  icon: Icon,
  className = '',
  type = 'button',
  onClick,
  ...props
}) {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-full transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 active:scale-95 disabled:opacity-50 disabled:pointer-events-none cursor-pointer';

  const variantStyles = {
    primary: 'bg-[#930500] text-[#FFF8E7] hover:bg-[#7a0400] focus:ring-[#930500] shadow-diffused-sm hover:shadow-editorial',
    secondary: 'bg-[#95BBEA] text-[#2B2523] hover:bg-[#83aa9] focus:ring-[#95BBEA] shadow-diffused-sm',
    outline: 'border border-[#930500] text-[#930500] hover:bg-[#930500] hover:text-[#FFF8E7] focus:ring-[#930500]',
    ghost: 'text-[#2B2523] hover:bg-[#rgba(147,5,0,0.05)] focus:ring-[#930500]',
    soft: 'bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] hover:bg-[#EFE7D3] focus:ring-[#95BBEA]',
  };

  const sizeStyles = {
    sm: 'px-4 py-1.5 text-xs gap-1.5',
    md: 'px-6 py-2.5 text-sm gap-2',
    lg: 'px-8 py-3.5 text-base gap-2.5 font-semibold',
  };

  return (
    <button
      type={type}
      disabled={disabled || isLoading}
      onClick={onClick}
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      {...props}
    >
      {isLoading ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : Icon ? (
        <Icon className="w-4 h-4" />
      ) : null}
      <span>{children}</span>
    </button>
  );
}
