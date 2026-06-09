/**
 * @fileoverview Badge component for status indicators and labels.
 */
import React from 'react';

type BadgeVariant = 'default' | 'primary' | 'success' | 'warning' | 'error' | 'info';
type BadgeSize = 'sm' | 'md';

interface BadgeProps {
  /** Badge text content */
  children: React.ReactNode;
  /** Visual variant */
  variant?: BadgeVariant;
  /** Size */
  size?: BadgeSize;
  /** Additional CSS classes */
  className?: string;
}

const variantStyles: Record<BadgeVariant, string> = {
  default: 'bg-dark-700 text-dark-300 border-dark-600',
  primary: 'bg-primary-600/20 text-primary-400 border-primary-600/30',
  success: 'bg-green-500/20 text-green-400 border-green-500/30',
  warning: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
  error: 'bg-red-500/20 text-red-400 border-red-500/30',
  info: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
};

const sizeStyles: Record<BadgeSize, string> = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
};

/**
 * Badge component for displaying status, labels, and categories.
 * @param props - Badge properties including variant, size
 */
const Badge = React.memo<BadgeProps>(function Badge({
  children,
  variant = 'default',
  size = 'sm',
  className = '',
}) {
  return (
    <span
      className={`
        inline-flex items-center font-medium rounded-full border
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${className}
      `.trim()}
    >
      {children}
    </span>
  );
});

export default Badge;
