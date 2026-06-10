import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Card from '../components/ui/Card';

describe('Card component', () => {
  it('renders children correctly', () => {
    render(<Card>Hello Card</Card>);
    expect(screen.getByText('Hello Card')).toBeInTheDocument();
  });

  it('applies variant classes', () => {
    const { container } = render(<Card variant="primary">Primary Card</Card>);
    expect(container.firstChild).toHaveClass('glass-primary');
  });

  it('applies padding classes', () => {
    const { container } = render(<Card padding="lg">Lg Card</Card>);
    expect(container.firstChild).toHaveClass('p-6');
  });
});
