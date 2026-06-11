/**
 * @fileoverview Unit tests for the Select component.
 */
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Select from '@/components/ui/Select';

const mockOptions = [
  { value: 'car', label: 'Car' },
  { value: 'bus', label: 'Bus' },
  { value: 'train', label: 'Train' },
];

describe('Select', () => {
  it('renders with a label', () => {
    render(<Select label="Transport" options={mockOptions} />);
    expect(screen.getByLabelText('Transport')).toBeInTheDocument();
  });

  it('renders all options', () => {
    render(<Select label="Transport" options={mockOptions} />);
    expect(screen.getByText('Car')).toBeInTheDocument();
    expect(screen.getByText('Bus')).toBeInTheDocument();
    expect(screen.getByText('Train')).toBeInTheDocument();
  });

  it('renders placeholder option when provided', () => {
    render(<Select label="Mode" options={mockOptions} placeholder="Select mode..." />);
    expect(screen.getByText('Select mode...')).toBeInTheDocument();
  });

  it('shows error message and sets aria-invalid', () => {
    render(<Select label="Mode" options={mockOptions} error="Required field" />);
    expect(screen.getByRole('alert')).toHaveTextContent('Required field');
    expect(screen.getByLabelText('Mode')).toHaveAttribute('aria-invalid', 'true');
  });

  it('sets aria-invalid to false when no error', () => {
    render(<Select label="Mode" options={mockOptions} />);
    expect(screen.getByLabelText('Mode')).toHaveAttribute('aria-invalid', 'false');
  });

  it('uses provided id for label association', () => {
    render(<Select label="Type" options={mockOptions} id="type-select" />);
    const select = screen.getByLabelText('Type');
    expect(select).toHaveAttribute('id', 'type-select');
  });

  it('passes through HTML select attributes', () => {
    render(<Select label="Mode" options={mockOptions} required disabled />);
    const select = screen.getByLabelText('Mode');
    expect(select).toBeRequired();
    expect(select).toBeDisabled();
  });
});
