/**
 * @fileoverview Accessible Select dropdown component with label and error state.
 */
import React, { useId, forwardRef } from 'react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  /** Select label text */
  label: string;
  /** Available options */
  options: SelectOption[];
  /** Error message */
  error?: string;
  /** Placeholder text */
  placeholder?: string;
}

/**
 * Accessible select dropdown with label, options, and error state.
 * @param props - Select properties including label, options, and error
 */
const Select = forwardRef<HTMLSelectElement, SelectProps>(function Select(
  { label, options, error, placeholder, className = '', id: propId, ...props },
  ref,
) {
  const generatedId = useId();
  const selectId = propId || generatedId;
  const errorId = `${selectId}-error`;

  return (
    <div className="space-y-1.5">
      <label
        htmlFor={selectId}
        className="block text-sm font-medium text-dark-300"
      >
        {label}
      </label>
      <select
        ref={ref}
        id={selectId}
        className={`
          w-full rounded-xl bg-dark-800 border text-dark-100
          transition-colors duration-200 appearance-none
          focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500
          px-4 py-3 text-sm cursor-pointer
          ${error ? 'border-error' : 'border-dark-600 hover:border-dark-500'}
          ${className}
        `.trim()}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : undefined}
        {...props}
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p id={errorId} className="text-sm text-error" role="alert">
          {error}
        </p>
      )}
    </div>
  );
});

export default Select;
