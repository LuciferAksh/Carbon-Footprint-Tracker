/**
 * @fileoverview Skeleton loading placeholder component.
 */
import React from 'react';

interface SkeletonProps {
  /** Width (CSS value or Tailwind class) */
  width?: string;
  /** Height (CSS value or Tailwind class) */
  height?: string;
  /** Shape variant */
  variant?: 'text' | 'circular' | 'rectangular' | 'rounded';
  /** Additional CSS classes */
  className?: string;
}

/**
 * Skeleton loading placeholder with pulse animation.
 * @param props - Skeleton properties including dimensions and shape variant
 */
const Skeleton = React.memo<SkeletonProps>(function Skeleton({
  width,
  height,
  variant = 'text',
  className = '',
}) {
  const shapeStyles: Record<string, string> = {
    text: 'rounded-md h-4',
    circular: 'rounded-full',
    rectangular: 'rounded-none',
    rounded: 'rounded-xl',
  };

  return (
    <div
      className={`animate-pulse bg-dark-700/60 ${shapeStyles[variant]} ${className}`}
      style={{ width, height }}
      aria-hidden="true"
      role="presentation"
    />
  );
});

export default Skeleton;
