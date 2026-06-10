import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import OnboardingQuiz from '../features/onboarding/OnboardingQuiz';

vi.mock('../features/auth/AuthProvider', () => ({
  useAuth: vi.fn().mockReturnValue({
    setOnboardingComplete: vi.fn(),
  }),
}));

vi.mock('../lib/api', () => ({
  api: {
    post: vi.fn().mockResolvedValue({ data: {} }),
  },
}));

describe('OnboardingQuiz component', () => {
  it('renders step 1 of onboarding quiz', () => {
    render(
      <MemoryRouter>
        <OnboardingQuiz />
      </MemoryRouter>,
    );

    expect(screen.getByText('Where are you located?')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /go to next step/i })).toBeInTheDocument();
  });

  it('navigates through steps when option selected and clicked continue', async () => {
    render(
      <MemoryRouter>
        <OnboardingQuiz />
      </MemoryRouter>,
    );

    // Click on 'India' option
    const indiaBtn = screen.getByRole('radio', { name: /india/i });
    fireEvent.click(indiaBtn);

    const continueBtn = screen.getByRole('button', { name: /go to next step/i });
    fireEvent.click(continueBtn);

    // Should navigate to step 2: "How big is your household?"
    expect(await screen.findByText('How big is your household?')).toBeInTheDocument();
  });
});
