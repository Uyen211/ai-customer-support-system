import React from 'react';

export function Input({
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
}) {
  const inputId = id || name;

  return (
    <div className={`w-full flex flex-col gap-1.5 ${className}`}>
      {label && (
        <label htmlFor={inputId} className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80">
          {label} {required && <span className="text-[#930500]">*</span>}
        </label>
      )}
      <div className="relative flex items-center">
        {Icon && (
          <div className="absolute left-4 text-[#2B2523]/50 pointer-events-none">
            <Icon className="w-5 h-5" />
          </div>
        )}
        <input
          id={inputId}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          className={`w-full bg-[#FFF8E7] text-[#2B2523] placeholder-[#2B2523]/40 border rounded-2xl py-3 text-sm transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-[#930500]/30 focus:border-[#930500] ${
            Icon ? 'pl-11 pr-4' : 'px-4'
          } ${error ? 'border-[#930500] ring-1 ring-[#930500]' : 'border-[#EFE7D3]'}`}
          {...props}
        />
      </div>
      {error && (
        <span className="text-xs text-[#930500] font-medium animate-fade-in pl-1">
          {error}
        </span>
      )}
    </div>
  );
}
