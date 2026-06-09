/**
 * @fileoverview Animated progress bar component for quizzes and challenges.
 */
import React from 'react';
import { motion } from 'framer-motion';

interface ProgressBarProps {
  /** Current progress value (0-100) */
  value: number;
  /** Maximum value (default: 100) */
  max?: number;
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
  /** Show percentage label */
  showLabel?: boolean;
  /** Color variant */
  color?: 'primary' | 'success' | 'warning' | 'error';
  /** Additional CSS classes */
  className?: string;
  /** Accessible label */
  ariaLabel?: string;
}

const sizeStyles: Record<string, string> = {
  sm: 'h-1.5',
  md: 'h-2.5',
  lg: 'h-4',
};

const colorStyles: Record<string, string> = {
  primary: 'bg-primary-500',
  success: 'bg-green-500',
  warning: 'bg-amber-500',
  error: 'bg-red-500',
};

/**
 * Animated progress bar with smooth transitions and accessibility.
 * @param props - ProgressBar properties including value, size, and color
 */
const ProgressBar = React.memo<ProgressBarProps>(function ProgressBar({
  value,
  max = 100,
  size = 'md',
  showLabel = false,
  color = 'primary',
  className = '',
  ariaLabel = 'Progress',
}) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  return (
    <div className={`space-y-1 ${className}`}>
      {showLabel && (
        <div className="flex justify-between text-xs text-dark-400">
          <span>{ariaLabel}</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
      <div
        className={`w-full bg-dark-800 rounded-full overflow-hidden ${sizeStyles[size]}`}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-label={ariaLabel}
      >
        <motion.div
          className={`h-full rounded-full ${colorStyles[color]}`}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
});

export default ProgressBar;
