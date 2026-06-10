import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ProgressBar from '../components/ui/ProgressBar';

describe('ProgressBar component', () => {
  it('renders correctly with default props', () => {
    render(<ProgressBar value={45} />);
    const bar = screen.getByRole('progressbar');
    expect(bar).toBeInTheDocument();
    expect(bar).toHaveAttribute('aria-valuenow', '45');
    expect(bar).toHaveAttribute('aria-valuemin', '0');
    expect(bar).toHaveAttribute('aria-valuemax', '100');
  });

  it('clamps value between 0 and max', () => {
    render(<ProgressBar value={150} max={100} />);
    const bar = screen.getByRole('progressbar');
    expect(bar).toHaveAttribute('aria-valuenow', '150');
  });

  it('renders label when showLabel is true', () => {
    render(<ProgressBar value={75} showLabel ariaLabel="Challenge Progress" />);
    expect(screen.getByText('Challenge Progress')).toBeInTheDocument();
    expect(screen.getByText('75%')).toBeInTheDocument();
  });
});
