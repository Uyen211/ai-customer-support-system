import React, { forwardRef } from 'react';
import { AlertCircle } from 'lucide-react';

export const Input = forwardRef(function Input(
  {
    label,
    error,
    type = 'text',
    placeholder,
    value,
    onChange,
    name,
    id,
    required = false,
    className = '',
    icon: Icon,
    ...props
  },
  ref
) {
  const inputId = id || name;

  return (
    <div className={`w-full flex flex-col gap-1.5 ${className}`}>
      {label && (
        <label
          htmlFor={inputId}
          className={`text-xs uppercase tracking-wider font-semibold transition-colors ${
            error ? 'text-[#930500]' : 'text-[#2B2523]/80'
          }`}
        >
          {label} {required && <span className="text-[#930500]">*</span>}
        </label>
      )}
      <div className="relative flex items-center">
        {Icon && (
          <div
            className={`absolute left-4 pointer-events-none transition-colors ${
              error ? 'text-[#930500]' : 'text-[#2B2523]/50'
            }`}
          >
            <Icon className="w-5 h-5" />
          </div>
        )}
        <input
          ref={ref}
          id={inputId}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          className={`w-full text-sm rounded-2xl py-3 transition-all duration-300 focus:outline-none ${
            Icon ? 'pl-11 pr-4' : 'px-4'
          } ${
            error
              ? 'bg-[#FFF5F5] border border-[#930500] ring-1 ring-[#930500] text-[#930500] placeholder-[#930500]/40 focus:ring-2 focus:ring-[#930500]/40 focus:border-[#930500]'
              : 'bg-[#FFF8E7] text-[#2B2523] placeholder-[#2B2523]/40 border border-[#EFE7D3] focus:ring-2 focus:ring-[#930500]/20 focus:border-[#930500]'
          }`}
          {...props}
        />
      </div>
      {error && (
        <p className="text-xs text-[#930500] font-medium flex items-center gap-1.5 animate-fade-in pl-1 mt-0.5">
          <AlertCircle className="w-3.5 h-3.5 shrink-0" />
          <span>{error}</span>
        </p>
      )}
    </div>
  );
});
