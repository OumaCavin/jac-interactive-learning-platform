// JAC Learning Platform - Advanced Button component by Cavin Otieno

import React from 'react';
import { motion, Variants } from 'framer-motion';

/**
 * Advanced Button component with glassmorphism design
 * Supports all variants including success, warning, error
 */

interface AdvancedButtonProps {
  // Custom component props
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  glass?: boolean;
  children: React.ReactNode;
  className?: string;
  disabled?: boolean;
  
  // Essential button attributes we want to support
  type?: 'button' | 'submit' | 'reset';
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLButtonElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLButtonElement>) => void;
  onKeyDown?: (event: React.KeyboardEvent<HTMLButtonElement>) => void;
  onKeyUp?: (event: React.KeyboardEvent<HTMLButtonElement>) => void;
  onKeyPress?: (event: React.KeyboardEvent<HTMLButtonElement>) => void;
  onMouseEnter?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  onMouseLeave?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  onTouchStart?: (event: React.TouchEvent<HTMLButtonElement>) => void;
  onTouchEnd?: (event: React.TouchEvent<HTMLButtonElement>) => void;
  id?: string;
  name?: string;
  value?: string;
  title?: string;
  ariaLabel?: string;
  ariaDescribedBy?: string;
  role?: string;
  tabIndex?: number;
  form?: string;
}

const buttonVariants: Variants = {
  initial: { scale: 1 },
  hover: { scale: 1.02 },
  tap: { scale: 0.98 },
};

export const AdvancedButton: React.FC<AdvancedButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  glass = true,
  children,
  className = '',
  disabled,
  type = 'button',
  onClick,
  onBlur,
  onFocus,
  onKeyDown,
  onKeyUp,
  onKeyPress,
  onMouseEnter,
  onMouseLeave,
  onTouchStart,
  onTouchEnd,
  id,
  name,
  value,
  title,
  ariaLabel,
  ariaDescribedBy,
  role,
  tabIndex,
  form,
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-white/30 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  const variantClasses = {
    primary: glass 
      ? 'glass-button-primary text-white shadow-glow' 
      : 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg hover:shadow-glow',
    secondary: glass
      ? 'glass text-white hover:bg-white/20'
      : 'bg-gradient-to-r from-secondary-500 to-secondary-600 text-white shadow-lg',
    success: glass
      ? 'glass text-white hover:bg-success-500/20'
      : 'bg-gradient-to-r from-success-500 to-success-600 text-white shadow-lg',
    warning: glass
      ? 'glass text-white hover:bg-warning-500/20'
      : 'bg-gradient-to-r from-warning-500 to-warning-600 text-white shadow-lg',
    error: glass
      ? 'glass text-white hover:bg-error-500/20'
      : 'bg-gradient-to-r from-error-500 to-error-600 text-white shadow-lg',
    ghost: 'text-white hover:bg-white/10',
  };

  const classes = `${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${className}`;

  return (
    <motion.button
      variants={buttonVariants}
      initial="initial"
      whileHover="hover"
      whileTap="tap"
      className={classes}
      disabled={disabled || isLoading}
      type={type}
      onClick={onClick}
      onBlur={onBlur}
      onFocus={onFocus}
      onKeyDown={onKeyDown}
      onKeyUp={onKeyUp}
      onKeyPress={onKeyPress}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onTouchStart={onTouchStart}
      onTouchEnd={onTouchEnd}
      id={id}
      name={name}
      value={value}
      title={title}
      aria-label={ariaLabel}
      aria-describedby={ariaDescribedBy}
      role={role}
      tabIndex={tabIndex}
      form={form}
    >
      {isLoading ? (
        <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin mr-2" />
      ) : leftIcon ? (
        <span className="mr-2">{leftIcon}</span>
      ) : null}
      {children}
      {!isLoading && rightIcon ? (
        <span className="ml-2">{rightIcon}</span>
      ) : null}
    </motion.button>
  );
};

export default AdvancedButton;