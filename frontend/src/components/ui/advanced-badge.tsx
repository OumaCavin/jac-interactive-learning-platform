// JAC Learning Platform - Advanced Badge component by Cavin Otieno

import React from 'react';

/**
 * Advanced Badge component with glassmorphism design
 * Supports glass prop and other advanced features
 */

interface AdvancedBadgeProps {
  variant?: 'primary' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md' | 'lg';
  glass?: boolean;
  children: React.ReactNode;
  className?: string;
}

export const AdvancedBadge: React.FC<AdvancedBadgeProps> = ({
  variant = 'primary',
  size = 'md',
  glass = true,
  children,
  className = '',
}) => {
  const variantClasses = {
    primary: glass ? 'glass text-primary-100' : 'bg-primary-500 text-white',
    success: glass ? 'glass text-success-100' : 'bg-success-500 text-white',
    warning: glass ? 'glass text-warning-100' : 'bg-warning-500 text-white',
    error: glass ? 'glass text-error-100' : 'bg-error-500 text-white',
    info: glass ? 'glass text-info-100' : 'bg-info-500 text-white',
  };

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base',
  };

  const classes = `inline-flex items-center font-medium rounded-full ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;

  return (
    <span className={classes}>
      {children}
    </span>
  );
};

export default AdvancedBadge;