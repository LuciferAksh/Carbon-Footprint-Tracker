/**
 * @fileoverview Reusable Button component with multiple variants and sizes.
 * Supports loading state, icons, and full ARIA accessibility.
 */
import React from 'react';
import { motion, type HTMLMotionProps } from 'framer-motion';

type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends Omit<HTMLMotionProps<'button'>, 'children'> {
  /** Button content */
  children: React.ReactNode;
  /** Visual variant */
  variant?: ButtonVariant;
  /** Size */
  size?: ButtonSize;
  /** Show loading spinner */
  loading?: boolean;
  /** Icon element to show before text */
  icon?: React.ReactNode;
  /** Make button full width */
  fullWidth?: boolean;
}

const variantStyles: Record<ButtonVariant, string> = {
  primary:
    'bg-primary-600 hover:bg-primary-500 text-white shadow-lg shadow-primary-600/25',
  secondary:
    'bg-dark-700 hover:bg-dark-600 text-dark-100 border border-dark-600',
  ghost:
    'bg-transparent hover:bg-dark-800 text-dark-300 hover:text-dark-100',
  danger:
    'bg-error hover:bg-red-500 text-white shadow-lg shadow-red-500/25',
  outline:
    'bg-transparent border-2 border-primary-600 text-primary-400 hover:bg-primary-600/10',
};

const sizeStyles: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-sm rounded-lg gap-1.5',
  md: 'px-5 py-2.5 text-sm rounded-xl gap-2',
  lg: 'px-7 py-3.5 text-base rounded-xl gap-2.5',
};

/**
 * Button component with motion animations, multiple variants, and accessibility.
 * @param props - Button properties including variant, size, loading state, and icon
 */
const Button = React.memo<ButtonProps>(function Button({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  fullWidth = false,
  className = '',
  disabled,
  ...props
}) {
  return (
    <motion.button
      whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
      whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
      className={`
        inline-flex items-center justify-center font-semibold
        transition-colors duration-200 cursor-pointer
        disabled:opacity-50 disabled:cursor-not-allowed
        focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${fullWidth ? 'w-full' : ''}
        ${className}
      `.trim()}
      disabled={disabled || loading}
      aria-busy={loading}
      {...props}
    >
      {loading ? (
        <svg
          className="animate-spin h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
          />
        </svg>
      ) : icon ? (
        <span aria-hidden="true">{icon}</span>
      ) : null}
      {children}
    </motion.button>
  );
});

export default Button;
