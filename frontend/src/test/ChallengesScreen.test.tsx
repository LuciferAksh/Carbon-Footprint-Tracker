import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ChallengesScreen from '../features/challenges/ChallengesScreen';
import { api } from '../lib/api';
import { ToastProvider } from '../components/ui/Toast';

vi.mock('../lib/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

const mockChallenges = [
  {
    id: '2026-W23',
    title: 'Metro Week Challenge',
    description: 'Take public transport at least 3 times this week.',
    category: 'transport',
    difficulty: 'medium',
    durationDays: 7,
    co2SavedTarget: 4.2,
    co2SavedActual: 1.8,
    progress: 43,
    status: 'active',
    participants: 234,
    tips: [],
  },
  {
    id: '2026-W22',
    title: 'Meatless Monday Champion',
    description: 'Go fully vegetarian on Monday.',
    category: 'food',
    difficulty: 'easy',
    durationDays: 7,
    co2SavedTarget: 5.3,
    co2SavedActual: 5.3,
    progress: 100,
    status: 'completed',
    participants: 412,
    tips: [],
  },
];

describe('ChallengesScreen component', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders list of active and past challenges', async () => {
    (api.get as any).mockResolvedValue({ data: mockChallenges });

    render(
      <MemoryRouter>
        <ToastProvider>
          <ChallengesScreen />
        </ToastProvider>
      </MemoryRouter>,
    );

    // Should display loading state first
    expect(screen.getByRole('status')).toBeInTheDocument();

    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('Metro Week Challenge')).toBeInTheDocument();
    });

    expect(screen.getByText('Meatless Monday Champion')).toBeInTheDocument();
    expect(screen.getByText('Get Custom AI Challenge')).toBeInTheDocument();
  });

  it('requests custom AI challenge suggestion and inserts it into active list', async () => {
    (api.get as any).mockResolvedValue({ data: [] });

    const suggestedChallenge = {
      id: '2026-W23',
      title: 'Solar Charged Week',
      description: 'Run major household appliances on solar energy peaks.',
      category: 'energy',
      difficulty: 'hard',
      durationDays: 7,
      co2SavedTarget: 6.0,
      co2SavedActual: 0.0,
      progress: 0,
      status: 'active',
      participants: 120,
      tips: [],
    };
    (api.post as any).mockResolvedValue({ data: suggestedChallenge });

    render(
      <MemoryRouter>
        <ToastProvider>
          <ChallengesScreen />
        </ToastProvider>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('Get Custom AI Challenge')).toBeInTheDocument();
    });

    const categorySelect = screen.getByLabelText(/Select category for AI challenge/i);
    const suggestBtn = screen.getByRole('button', { name: /Suggest Challenge/i });

    // Select Energy category and click suggest
    fireEvent.change(categorySelect, { target: { value: 'energy' } });
    fireEvent.click(suggestBtn);

    // Verify loading state and success message
    await waitFor(() => {
      expect(screen.getByText('Solar Charged Week')).toBeInTheDocument();
    });
    expect(api.post).toHaveBeenCalledWith('/challenge/suggest/energy', {});
  });
});
