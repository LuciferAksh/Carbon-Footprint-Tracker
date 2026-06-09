/**
 * @fileoverview React Error Boundary component for catching render errors.
 * Shows a friendly error UI with retry option.
 */
import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface ErrorBoundaryProps {
  /** Child components to wrap */
  children: React.ReactNode;
  /** Optional fallback UI */
  fallback?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

/**
 * Error boundary component that catches JavaScript errors in child components.
 * Displays a retry-friendly error screen with the error message.
 */
class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    console.error('Error boundary caught:', error, errorInfo);
  }

  handleRetry = (): void => {
    this.setState({ hasError: false, error: null });
  };

  render(): React.ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div
          className="min-h-[50vh] flex items-center justify-center p-6"
          role="alert"
        >
          <div className="glass rounded-2xl p-8 max-w-md w-full text-center space-y-4">
            <div className="w-16 h-16 rounded-full bg-error/10 flex items-center justify-center mx-auto">
              <AlertTriangle className="w-8 h-8 text-error" aria-hidden="true" />
            </div>
            <h2 className="text-xl font-bold text-dark-100">
              Something went wrong
            </h2>
            <p className="text-sm text-dark-400">
              {this.state.error?.message || 'An unexpected error occurred. Please try again.'}
            </p>
            <button
              onClick={this.handleRetry}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-600 hover:bg-primary-500 text-white rounded-xl font-semibold text-sm transition-colors cursor-pointer"
              aria-label="Retry loading this page"
            >
              <RefreshCw className="w-4 h-4" aria-hidden="true" />
              Try Again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
