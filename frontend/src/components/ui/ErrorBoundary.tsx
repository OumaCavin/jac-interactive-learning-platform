// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React from 'react';

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    console.error('Error stack:', error.stack);
    console.error('Component stack:', errorInfo.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="glass-strong rounded-2xl p-8 max-w-md w-full text-center">
            <h2 className="text-xl font-bold text-white mb-4">Something went wrong</h2>
            <p className="text-white/80 mb-6">
              We're sorry, but something unexpected happened. Please try refreshing the page.
            </p>
            
            {this.state.error && (
              <details className="mb-6 text-left">
                <summary className="text-white/80 cursor-pointer">Error Details</summary>
                <div className="mt-2 p-3 bg-black/20 rounded text-white/70 text-sm font-mono">
                  {this.state.error.message}
                </div>
              </details>
            )}
            
            <button
              onClick={() => window.location.reload()}
              className="glass-button-primary mr-3"
            >
              Refresh Page
            </button>
            
            <button
              onClick={() => {
                localStorage.clear();
                window.location.reload();
              }}
              className="glass-button-secondary"
            >
              Clear Storage & Refresh
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}