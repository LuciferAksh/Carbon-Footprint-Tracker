import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import LogScreen from '../features/activity-log/LogScreen';

vi.mock('../components/ui/Toast', () => ({
  useToast: vi.fn().mockReturnValue({
    addToast: vi.fn(),
  }),
}));

vi.mock('../lib/api', () => ({
  api: {
    post: vi.fn().mockResolvedValue({ data: { tip: 'Use public transport' } }),
  },
}));

describe('LogScreen component', () => {
  it('renders default empty state asking to select category', () => {
    render(<LogScreen />);
    expect(screen.getByText(/Tap a category above to start logging/i)).toBeInTheDocument();
  });

  it('opens details form when category tile is clicked', () => {
    render(<LogScreen />);

    // Select Transport category button
    const transportBtn = screen.getByRole('button', { name: /log transport activity/i });
    fireEvent.click(transportBtn);

    expect(screen.getByText(/Add Transport/i)).toBeInTheDocument();
  });
});
