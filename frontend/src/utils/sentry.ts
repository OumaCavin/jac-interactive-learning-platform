// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Simple error handling utilities (Sentry disabled)
 */

import React from 'react';

/**
 * Initialize error monitoring (placeholder)
 */
export function initSentry() {
  console.warn("Error monitoring not configured - using fallback implementation");
}

/**
 * Simple error interface
 */
interface ErrorInfo {
  componentStack: string;
}

/**
 * Error boundary class component
 */
export class ErrorBoundary {
  private hasError: boolean = false;
  private error: Error | null = null;
  private resetError: () => void;

  constructor(private children: React.ReactNode, private fallback?: React.ComponentType<{ error: Error; resetError: () => void }>) {
    this.resetError = this.handleResetError.bind(this);
  }

  static getDerivedStateFromError(error: Error): { hasError: boolean; error: Error } {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    this.hasError = true;
    this.error = error;
  }

  private handleResetError() {
    this.hasError = false;
    this.error = null;
  }

  render() {
    if (this.hasError && this.error) {
      if (this.fallback) {
        const FallbackComponent = this.fallback;
        // eslint-disable-next-line react/jsx-filename-extension
        return React.createElement(FallbackComponent, { error: this.error, resetError: this.resetError });
      }
      
      // eslint-disable-next-line react/jsx-filename-extension
      return React.createElement('div', { className: 'error-boundary p-8 text-center' },
        React.createElement('h2', { className: 'text-xl font-bold text-red-600 mb-4' }, 'Something went wrong'),
        React.createElement('p', { className: 'text-gray-600 mb-4' }, this.error.message),
        React.createElement('button', { 
          onClick: this.resetError,
          className: 'bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
        }, 'Try again')
      );
    }

    return this.children;
  }
}

/**
 * Simple error boundary for React components
 */
export function SimpleErrorBoundary({ children, fallback }: { children: React.ReactNode; fallback?: React.ComponentType<{ error: Error; resetError: () => void }> }) {
  return new ErrorBoundary(children, fallback).render();
}

/**
 * Higher-order component for error tracking (simplified)
 */
export function withErrorTracking<P extends object>(
  WrappedComponent: React.ComponentType<P>
): React.ComponentType<P> {
  // For now, return the component as-is to avoid build issues
  return WrappedComponent;
}