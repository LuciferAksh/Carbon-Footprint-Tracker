/**
 * @fileoverview Glassmorphism Card component with hover effects and animation.
 */
import React from 'react';
import { motion, type HTMLMotionProps } from 'framer-motion';

interface CardProps extends HTMLMotionProps<'div'> {
  /** Card content */
  children: React.ReactNode;
  /** Glass effect variant */
  variant?: 'default' | 'primary' | 'light';
  /** Whether card has hover animation */
  hoverable?: boolean;
  /** Optional padding override */
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const variantStyles: Record<string, string> = {
  default: 'glass',
  primary: 'glass-primary',
  light: 'glass-light',
};

const paddingStyles: Record<string, string> = {
  none: '',
  sm: 'p-3',
  md: 'p-4 sm:p-5',
  lg: 'p-6 sm:p-8',
};

/**
 * Glassmorphism Card component with subtle border, backdrop blur, and optional hover effects.
 * @param props - Card properties including variant, hoverable, and padding
 */
const Card = React.memo<CardProps>(function Card({
  children,
  variant = 'default',
  hoverable = false,
  padding = 'md',
  className = '',
  ...props
}) {
  return (
    <motion.div
      whileHover={hoverable ? { y: -2, scale: 1.01 } : undefined}
      className={`
        rounded-2xl ${variantStyles[variant]} ${paddingStyles[padding]}
        ${hoverable ? 'cursor-pointer transition-shadow hover:shadow-lg hover:shadow-primary-600/5' : ''}
        ${className}
      `.trim()}
      {...props}
    >
      {children}
    </motion.div>
  );
});

export default Card;
