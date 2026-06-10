/**
 * @fileoverview Loading spinner component with multiple sizes.
 */
import React from 'react';
import { Leaf } from 'lucide-react';

interface LoadingSpinnerProps {
  /** Size of the spinner */
  size?: 'sm' | 'md' | 'lg';
  /** Optional message below spinner */
  message?: string;
  /** Whether to show full-screen centered */
  fullScreen?: boolean;
}

const sizeMap = {
  sm: 'w-5 h-5',
  md: 'w-8 h-8',
  lg: 'w-12 h-12',
};

/**
 * Loading spinner with animated leaf icon and optional message.
 * @param props - Spinner properties including size, message, and fullScreen mode
 */
const LoadingSpinner = React.memo<LoadingSpinnerProps>(function LoadingSpinner({
  size = 'md',
  message,
  fullScreen = false,
}) {
  const content = (
    <div className="flex flex-col items-center gap-3" role="status" aria-label="Loading" aria-live="polite">
      <Leaf className={`${sizeMap[size]} text-primary-500 animate-spin`} aria-hidden="true" />
      {message && <p className="text-sm text-dark-400 animate-pulse">{message}</p>}
      <span className="sr-only">Loading...</span>
    </div>
  );

  if (fullScreen) {
    return (
      <div className="min-h-dvh flex items-center justify-center gradient-dark">{content}</div>
    );
  }

  return <div className="flex items-center justify-center py-12">{content}</div>;
});

export default LoadingSpinner;
