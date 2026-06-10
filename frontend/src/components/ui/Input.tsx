/**
 * @fileoverview Accessible Input component with label, error state, and icons.
 */
import React, { useId, forwardRef } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Input label text */
  label: string;
  /** Error message */
  error?: string;
  /** Helper text below input */
  helperText?: string;
  /** Icon element to show on the left */
  icon?: React.ReactNode;
}

/**
 * Accessible text input with label, validation error display, and optional icon.
 * @param props - Input properties including label, error, helperText, and icon
 */
const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { label, error, helperText, icon, className = '', id: propId, ...props },
  ref,
) {
  const generatedId = useId();
  const inputId = propId || generatedId;
  const errorId = `${inputId}-error`;
  const helperId = `${inputId}-helper`;

  return (
    <div className="space-y-1.5">
      <label htmlFor={inputId} className="block text-sm font-medium text-dark-300">
        {label}
      </label>
      <div className="relative">
        {icon && (
          <span
            className="absolute left-3 top-1/2 -translate-y-1/2 text-dark-400"
            aria-hidden="true"
          >
            {icon}
          </span>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`
            w-full rounded-xl bg-dark-800 border text-dark-100 placeholder-dark-500
            transition-colors duration-200
            focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500
            ${icon ? 'pl-10' : 'pl-4'} pr-4 py-3 text-sm
            ${error ? 'border-error' : 'border-dark-600 hover:border-dark-500'}
            ${className}
          `.trim()}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? errorId : helperText ? helperId : undefined}
          {...props}
        />
      </div>
      {error && (
        <p id={errorId} className="text-sm text-error flex items-center gap-1" role="alert">
          <svg
            className="w-3.5 h-3.5 shrink-0"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
          {error}
        </p>
      )}
      {helperText && !error && (
        <p id={helperId} className="text-xs text-dark-500">
          {helperText}
        </p>
      )}
    </div>
  );
});

export default Input;
