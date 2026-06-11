/**
 * @fileoverview Unit tests for the Skeleton component.
 */
import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Skeleton from '@/components/ui/Skeleton';

describe('Skeleton', () => {
  it('renders with aria-hidden', () => {
    const { container } = render(<Skeleton />);
    const el = container.firstChild as HTMLElement;
    expect(el).toHaveAttribute('aria-hidden', 'true');
  });

  it('has role="presentation"', () => {
    const { container } = render(<Skeleton />);
    const el = container.firstChild as HTMLElement;
    expect(el).toHaveAttribute('role', 'presentation');
  });

  it('applies animate-pulse class', () => {
    const { container } = render(<Skeleton />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('animate-pulse');
  });

  it('applies default text variant (rounded-md)', () => {
    const { container } = render(<Skeleton />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('rounded-md');
  });

  it('applies circular variant', () => {
    const { container } = render(<Skeleton variant="circular" />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('rounded-full');
  });

  it('applies rectangular variant', () => {
    const { container } = render(<Skeleton variant="rectangular" />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('rounded-none');
  });

  it('applies rounded variant', () => {
    const { container } = render(<Skeleton variant="rounded" />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('rounded-xl');
  });

  it('applies custom width and height via style', () => {
    const { container } = render(<Skeleton width="100px" height="20px" />);
    const el = container.firstChild as HTMLElement;
    expect(el.style.width).toBe('100px');
    expect(el.style.height).toBe('20px');
  });

  it('merges additional className', () => {
    const { container } = render(<Skeleton className="my-4 w-48" />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('my-4');
    expect(el.className).toContain('w-48');
  });
});
