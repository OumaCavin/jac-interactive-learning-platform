// JAC Learning Platform - Advanced Input component by Cavin Otieno

import React from 'react';

/**
 * Advanced Input component with glassmorphism design
 * Supports label, error, and icon props
 */

interface AdvancedInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  glass?: boolean;
}

export const AdvancedInput: React.FC<AdvancedInputProps> = ({
  label,
  error,
  leftIcon,
  rightIcon,
  glass = true,
  className = '',
  ...props
}) => {
  const inputClasses = glass
    ? 'glass rounded-xl px-4 py-3 text-white placeholder-white/80 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent'
    : 'bg-white/10 backdrop-blur-md rounded-xl px-4 py-3 text-white placeholder-white/80 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent';

  const baseClasses = 'w-full transition-all duration-200';
  const errorClasses = error ? 'border-error-500' : 'border-transparent';

  return (
    <div className={`${baseClasses} ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-white mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        {leftIcon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span className="text-white/80">{leftIcon}</span>
          </div>
        )}
        <input
          className={`${inputClasses} ${errorClasses} ${leftIcon ? 'pl-10' : ''} ${rightIcon ? 'pr-10' : ''}`}
          {...props}
        />
        {rightIcon && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            <span className="text-white/80">{rightIcon}</span>
          </div>
        )}
      </div>
      {error && (
        <p className="mt-1 text-sm text-error-400">{error}</p>
      )}
    </div>
  );
};

export default AdvancedInput;