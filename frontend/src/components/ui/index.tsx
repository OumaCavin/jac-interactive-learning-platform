/**
 * Basic UI components with glassmorphism design
 * Provides reusable components following the design system
 */

import React from 'react';
import { motion, Variants } from 'framer-motion';

// Loading Spinner Component
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  size = 'md', 
  className = '' 
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  };

  return (
    <div className={`flex items-center justify-center ${className}`}>
      <div 
        className={`${sizeClasses[size]} border-2 border-white/20 border-t-white rounded-full animate-spin`}
        role="status"
        aria-label="Loading"
      >
        <span className="sr-only">Loading...</span>
      </div>
    </div>
  );
};

// Button Component
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  glass?: boolean;
  children: React.ReactNode;
}

const buttonVariants: Variants = {
  initial: { scale: 1 },
  hover: { scale: 1.02 },
  tap: { scale: 0.98 },
};

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  glass = true,
  children,
  className = '',
  disabled,
  ...restProps
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
      {...restProps}
    >
      {isLoading ? (
        <LoadingSpinner size="sm" className="mr-2" />
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

// Card Component
interface CardProps {
  variant?: 'glass' | 'glass-strong' | 'solid';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  className?: string;
  children: React.ReactNode;
  hover?: boolean;
  onClick?: () => void;
}

const cardVariants: Variants = {
  initial: { y: 0, opacity: 1 },
  hover: { y: -4, opacity: 1 },
};

export const Card: React.FC<CardProps> = ({
  variant = 'glass',
  padding = 'md',
  className = '',
  children,
  hover = false,
  onClick,
}) => {
  const baseClasses = 'rounded-2xl transition-all duration-300';
  
  const variantClasses = {
    glass: 'glass-card',
    'glass-strong': 'glass-card-strong',
    solid: 'bg-white/10 backdrop-blur-md border border-white/20',
  };

  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${paddingClasses[padding]} ${className}`;

  if (onClick) {
    return (
      <motion.div
        variants={hover ? cardVariants : undefined}
        initial="initial"
        whileHover="hover"
        className={`${classes} cursor-pointer`}
        onClick={onClick}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      variants={hover ? cardVariants : undefined}
      initial="initial"
      whileHover="hover"
      className={classes}
    >
      {children}
    </motion.div>
  );
};

// Input Component
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  glass?: boolean;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  leftIcon,
  rightIcon,
  glass = true,
  className = '',
  ...props
}) => {
  const inputClasses = glass
    ? 'glass rounded-xl px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent'
    : 'bg-white/10 backdrop-blur-md rounded-xl px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent';

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
            <span className="text-white/50">{leftIcon}</span>
          </div>
        )}
        <input
          className={`${inputClasses} ${errorClasses} ${leftIcon ? 'pl-10' : ''} ${rightIcon ? 'pr-10' : ''}`}
          {...props}
        />
        {rightIcon && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            <span className="text-white/50">{rightIcon}</span>
          </div>
        )}
      </div>
      {error && (
        <p className="mt-1 text-sm text-error-400">{error}</p>
      )}
    </div>
  );
};

// Progress Bar Component
interface ProgressBarProps {
  value: number; // 0-100
  max?: number;
  variant?: 'primary' | 'success' | 'warning' | 'error';
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  variant = 'primary',
  size = 'md',
  showLabel = false,
  className = '',
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  
  const variantClasses = {
    primary: 'bg-gradient-to-r from-primary-400 to-primary-600',
    success: 'bg-gradient-to-r from-success-400 to-success-600',
    warning: 'bg-gradient-to-r from-warning-400 to-warning-600',
    error: 'bg-gradient-to-r from-error-400 to-error-600',
  };

  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  };

  return (
    <div className={`w-full ${className}`}>
      {showLabel && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-white/80">Progress</span>
          <span className="text-sm text-white">{percentage.toFixed(1)}%</span>
        </div>
      )}
      <div className={`progress-glass ${sizeClasses[size]}`}>
        <motion.div
          className={`progress-fill ${variantClasses[variant]}`}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
};

// Badge Component
interface BadgeProps {
  variant?: 'primary' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md' | 'lg';
  glass?: boolean;
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
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

// Error Boundary Component
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<
  React.PropsWithChildren<{}>,
  ErrorBoundaryState
> {
  constructor(props: React.PropsWithChildren<{}>) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="glass-strong rounded-2xl p-8 max-w-md w-full text-center">
            <h2 className="text-xl font-bold text-white mb-4">Something went wrong</h2>
            <p className="text-white/80 mb-6">
              We&apos;re sorry, but something unexpected happened. Please try refreshing the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="glass-button-primary"
            >
              Refresh Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}