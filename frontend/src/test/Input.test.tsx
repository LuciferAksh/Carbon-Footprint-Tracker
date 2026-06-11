/**
 * @fileoverview Unit tests for the Input component.
 */
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Input from '@/components/ui/Input';

describe('Input', () => {
  it('renders with a label', () => {
    render(<Input label="Email" />);
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
  });

  it('renders the label text', () => {
    render(<Input label="Username" />);
    expect(screen.getByText('Username')).toBeInTheDocument();
  });

  it('shows error message and sets aria-invalid', () => {
    render(<Input label="Name" error="Name is required" />);
    expect(screen.getByRole('alert')).toHaveTextContent('Name is required');
    expect(screen.getByLabelText('Name')).toHaveAttribute('aria-invalid', 'true');
  });

  it('sets aria-invalid to false when no error', () => {
    render(<Input label="Name" />);
    expect(screen.getByLabelText('Name')).toHaveAttribute('aria-invalid', 'false');
  });

  it('renders helper text when provided and no error', () => {
    render(<Input label="Email" helperText="We'll never share your email" />);
    expect(screen.getByText("We'll never share your email")).toBeInTheDocument();
  });

  it('hides helper text when error is present', () => {
    render(<Input label="Email" helperText="Optional" error="Invalid email" />);
    expect(screen.queryByText('Optional')).not.toBeInTheDocument();
    expect(screen.getByText('Invalid email')).toBeInTheDocument();
  });

  it('renders icon slot', () => {
    render(<Input label="Search" icon={<span data-testid="search-icon">🔍</span>} />);
    expect(screen.getByTestId('search-icon')).toBeInTheDocument();
  });

  it('uses provided id for label association', () => {
    render(<Input label="Custom" id="custom-input" />);
    const input = screen.getByLabelText('Custom');
    expect(input).toHaveAttribute('id', 'custom-input');
  });

  it('passes through HTML input attributes', () => {
    render(<Input label="Quantity" type="number" min="0" placeholder="Enter amount" />);
    const input = screen.getByLabelText('Quantity');
    expect(input).toHaveAttribute('type', 'number');
    expect(input).toHaveAttribute('min', '0');
    expect(input).toHaveAttribute('placeholder', 'Enter amount');
  });
});
