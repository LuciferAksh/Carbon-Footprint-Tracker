/**
 * @fileoverview Unit tests for the Badge component.
 */
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Badge from '@/components/ui/Badge';

describe('Badge', () => {
  it('renders children text', () => {
    render(<Badge>Active</Badge>);
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('applies default variant styles', () => {
    const { container } = render(<Badge>Default</Badge>);
    const span = container.querySelector('span');
    expect(span?.className).toContain('bg-dark-700');
  });

  it('applies primary variant styles', () => {
    const { container } = render(<Badge variant="primary">Primary</Badge>);
    const span = container.querySelector('span');
    expect(span?.className).toContain('bg-primary-600/20');
  });

  it('applies success variant styles', () => {
    const { container } = render(<Badge variant="success">Completed</Badge>);
    const span = container.querySelector('span');
    expect(span?.className).toContain('bg-green-500/20');
  });

  it('applies sm size by default', () => {
    const { container } = render(<Badge>Small</Badge>);
    const span = container.querySelector('span');
    expect(span?.className).toContain('text-xs');
  });

  it('applies md size when specified', () => {
    const { container } = render(<Badge size="md">Medium</Badge>);
    const span = container.querySelector('span');
    expect(span?.className).toContain('text-sm');
  });

  it('merges additional className', () => {
    const { container } = render(<Badge className="mt-2">Custom</Badge>);
    const span = container.querySelector('span');
    expect(span?.className).toContain('mt-2');
  });

  it('renders with React node children', () => {
    render(
      <Badge variant="primary">
        <span data-testid="icon">🌱</span> Eco
      </Badge>,
    );
    expect(screen.getByTestId('icon')).toBeInTheDocument();
    expect(screen.getByText('Eco')).toBeInTheDocument();
  });
});
