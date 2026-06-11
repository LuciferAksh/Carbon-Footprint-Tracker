/**
 * @fileoverview Unit tests for the DashboardScreen component.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import DashboardScreen from '../features/dashboard/DashboardScreen';
import { api } from '../lib/api';

vi.mock('../lib/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

vi.mock('../features/auth', () => ({
  useAuth: () => ({
    user: { displayName: 'Test User', email: 'test@test.com' },
    loading: false,
  }),
}));

const mockDashboardData = {
  totalCO2Today: 4.2,
  totalCO2Week: 28.5,
  totalCO2Month: 112.3,
  weeklyComparison: [
    { day: 'Mon', thisWeek: 4.1, lastWeek: 5.2 },
    { day: 'Tue', thisWeek: 3.8, lastWeek: 4.5 },
    { day: 'Wed', thisWeek: 5.0, lastWeek: 4.8 },
    { day: 'Thu', thisWeek: 4.2, lastWeek: 5.1 },
    { day: 'Fri', thisWeek: 3.5, lastWeek: 4.3 },
    { day: 'Sat', thisWeek: 3.9, lastWeek: 4.0 },
    { day: 'Sun', thisWeek: 4.0, lastWeek: 3.8 },
  ],
  categoryBreakdown: [
    { category: 'transport', amount: 12.5, percentage: 44.3, color: '#3b82f6' },
    { category: 'food', amount: 8.2, percentage: 29.1, color: '#f59e0b' },
    { category: 'energy', amount: 5.1, percentage: 18.1, color: '#a855f7' },
    { category: 'shopping', amount: 2.7, percentage: 9.6, color: '#ec4899' },
  ],
  streak: 5,
  carbonScore: 78,
  benchmark: {
    user: 2100.0,
    national: 2500.0,
    target: 1500.0,
  },
};

const mockChallenge = {
  id: '2026-W24',
  title: 'Green Commuter Week',
  description: 'Take public transit for all commutes.',
  category: 'transport',
  difficulty: 'easy',
  durationDays: 7,
  co2SavedTarget: 6.5,
  co2SavedActual: 2.1,
  progress: 32,
  status: 'active',
  participants: 154,
  tips: [],
};

describe('DashboardScreen component', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders loading state initially then displays dashboard data', async () => {
    (api.get as ReturnType<typeof vi.fn>).mockImplementation((endpoint: string) => {
      if (endpoint.includes('/activity/summary')) {
        return Promise.resolve({ data: mockDashboardData });
      }
      if (endpoint.includes('/challenge/current')) {
        return Promise.resolve({ data: mockChallenge });
      }
      return Promise.resolve({ data: {} });
    });

    render(
      <MemoryRouter>
        <DashboardScreen />
      </MemoryRouter>,
    );

    // Initially shows loading skeleton
    expect(screen.getByText(/Loading dashboard/i)).toBeInTheDocument();
    expect(screen.getByRole('status')).toBeInTheDocument();

    // After loading, dashboard content appears
    await waitFor(
      () => {
        expect(screen.getByText(/My Carbon Story/i)).toBeInTheDocument();
      },
      { timeout: 3000 },
    );

    // Check main data sections render
    expect(screen.getByText(/This Week's Footprint/i)).toBeInTheDocument();
    expect(screen.getByText(/Today/i)).toBeInTheDocument();
  });

  it('renders loading skeletons with accessible status before data arrives', () => {
    // Make API hang indefinitely
    (api.get as ReturnType<typeof vi.fn>).mockReturnValue(new Promise(() => {}));

    render(
      <MemoryRouter>
        <DashboardScreen />
      </MemoryRouter>,
    );

    // Should show accessible loading indicator
    expect(screen.getByRole('status')).toBeInTheDocument();
    expect(screen.getByText(/Loading dashboard/i)).toBeInTheDocument();
  });

  it('displays challenge card after data loads', async () => {
    (api.get as ReturnType<typeof vi.fn>).mockImplementation((endpoint: string) => {
      if (endpoint.includes('/activity/summary')) {
        return Promise.resolve({ data: mockDashboardData });
      }
      if (endpoint.includes('/challenge/current')) {
        return Promise.resolve({ data: mockChallenge });
      }
      return Promise.resolve({ data: {} });
    });

    render(
      <MemoryRouter>
        <DashboardScreen />
      </MemoryRouter>,
    );

    await waitFor(
      () => {
        expect(screen.getByText(/Green Commuter Week/i)).toBeInTheDocument();
      },
      { timeout: 3000 },
    );
  });
});
