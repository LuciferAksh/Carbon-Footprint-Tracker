import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CoachScreen from '../features/coach/CoachScreen';
import { api } from '../lib/api';

vi.mock('../lib/api', () => ({
  api: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

describe('CoachScreen component', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders initial state with coach greeting and quick prompts', () => {
    render(<CoachScreen />);

    expect(screen.getByText(/CarbonCoach AI/i)).toBeInTheDocument();
    expect(screen.getByText(/Hello! I'm your CarbonCoach/i)).toBeInTheDocument();
    expect(screen.getByText('How do I lower my food footprint?')).toBeInTheDocument();
  });

  it('sends message and renders AI response correctly', async () => {
    const mockReply = 'Try using the metro to reduce emissions.';
    (api.post as any).mockResolvedValue({ data: { reply: mockReply } });

    render(<CoachScreen />);

    const input = screen.getByPlaceholderText(/Ask CarbonCoach.../i);
    const sendBtn = screen.getByRole('button', { name: /send message/i });

    // Type a message
    fireEvent.change(input, { target: { value: 'How can I save carbon?' } });
    fireEvent.click(sendBtn);

    // Verify user message is displayed immediately
    expect(screen.getByText('How can I save carbon?')).toBeInTheDocument();

    // Verify AI response displays after API call resolves
    await waitFor(() => {
      expect(screen.getByText(mockReply)).toBeInTheDocument();
    });

    expect(api.post).toHaveBeenCalledWith('/insights/chat', expect.any(Object));
  });

  it('allows playing the eco-quiz through to completion and restarting', async () => {
    render(<CoachScreen />);

    // Switch to quiz tab
    const quizTab = screen.getByRole('button', { name: /Play Eco-Quiz/i });
    fireEvent.click(quizTab);

    // Verify start screen is shown
    await waitFor(() => {
      expect(screen.getByText('Eco-Quiz Challenge')).toBeInTheDocument();
    });

    // Click "Play Now"
    const playBtn = screen.getByRole('button', { name: /Play Now/i });
    fireEvent.click(playBtn);

    // 1. Question 1
    await waitFor(() => {
      expect(
        screen.getByText(/Which of the following diets has the lowest average carbon footprint/i),
      ).toBeInTheDocument();
    });
    const q1Option = screen.getByRole('button', { name: /Fully vegan diet/i });
    fireEvent.click(q1Option);
    expect(screen.getByText(/CarbonCoach Insight/i)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Next Question/i }));

    // 2. Question 2
    await waitFor(() => {
      expect(
        screen.getByText(/How much energy\/CO₂ does a typical LED bulb save/i),
      ).toBeInTheDocument();
    });
    const q2Option = screen.getByRole('button', { name: /About 75% to 80%/i });
    fireEvent.click(q2Option);
    fireEvent.click(screen.getByRole('button', { name: /Next Question/i }));

    // 3. Question 3
    await waitFor(() => {
      expect(
        screen.getByText(
          /For a 10 km daily commute, which transport mode has the highest emissions/i,
        ),
      ).toBeInTheDocument();
    });
    const q3Option = screen.getByRole('button', { name: /Single-occupant petrol car/i });
    fireEvent.click(q3Option);
    fireEvent.click(screen.getByRole('button', { name: /Next Question/i }));

    // 4. Question 4
    await waitFor(() => {
      expect(
        screen.getByText(/What does the term "Phantom energy drain" refer to/i),
      ).toBeInTheDocument();
    });
    const q4Option = screen.getByRole('button', {
      name: /Electricity consumed by devices plugged in on standby mode/i,
    });
    fireEvent.click(q4Option);
    fireEvent.click(screen.getByRole('button', { name: /Next Question/i }));

    // 5. Question 5
    await waitFor(() => {
      expect(
        screen.getByText(
          /Which action has the highest single impact on reducing household carbon emissions/i,
        ),
      ).toBeInTheDocument();
    });
    const q5Option = screen.getByRole('button', {
      name: /Switching to a 100% renewable energy tariff or solar panels/i,
    });
    fireEvent.click(q5Option);

    // Verify finish button is visible on last question
    const finishBtn = screen.getByRole('button', { name: /Finish Quiz/i });
    fireEvent.click(finishBtn);

    // Verify finished screen is visible and shows perfect score
    await waitFor(() => {
      expect(screen.getByText(/Climate Hero!/i)).toBeInTheDocument();
    });
    expect(screen.getByText(/You scored 5 out of 5/i)).toBeInTheDocument();

    // Verify restarting works
    const playAgainBtn = screen.getByRole('button', { name: /Play Again/i });
    fireEvent.click(playAgainBtn);
    await waitFor(() => {
      expect(
        screen.getByText(/Which of the following diets has the lowest average carbon footprint/i),
      ).toBeInTheDocument();
    });
  });

  it('fetches dynamic questions from Vertex AI when starting the quiz', async () => {
    const mockQuestion1 = {
      id: 201,
      question: 'What is the primary greenhouse gas emitted by burning fossil fuels?',
      options: ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Helium'],
      correctAnswer: 1,
      explanation:
        'Carbon dioxide (CO2) is released in massive amounts from burning fossil fuels like coal, oil, and gas.',
    };
    const mockQuestion2 = {
      id: 202,
      question: 'Which transport mode has the lowest carbon footprint?',
      options: [
        'Driving a petrol car',
        'Flying in a commercial jet',
        'Riding a bicycle',
        'Taking a diesel train',
      ],
      correctAnswer: 2,
      explanation:
        'Riding a bicycle has a near-zero carbon footprint, except for the calories consumed to power it!',
    };

    (api.get as any).mockResolvedValueOnce({
      data: [
        mockQuestion1,
        mockQuestion2,
        { ...mockQuestion1, id: 203, question: 'Q3' },
        { ...mockQuestion1, id: 204, question: 'Q4' },
        { ...mockQuestion1, id: 205, question: 'Q5' },
      ],
    });

    render(<CoachScreen />);

    // Switch to quiz tab
    const quizTab = screen.getByRole('button', { name: /Play Eco-Quiz/i });
    fireEvent.click(quizTab);

    // Verify start screen is shown
    await waitFor(() => {
      expect(screen.getByText('Eco-Quiz Challenge')).toBeInTheDocument();
    });

    // Click "Play Now"
    const playBtn = screen.getByRole('button', { name: /Play Now/i });
    fireEvent.click(playBtn);

    // Verify dynamic question 1 is loaded
    await waitFor(() => {
      expect(screen.getByText(mockQuestion1.question)).toBeInTheDocument();
    });

    const option = screen.getByRole('button', { name: /Carbon Dioxide/i });
    fireEvent.click(option);

    expect(screen.getByText(/CarbonCoach Insight/i)).toBeInTheDocument();
    expect(screen.getByText(mockQuestion1.explanation)).toBeInTheDocument();

    const nextBtn = screen.getByRole('button', { name: /Next Question/i });
    fireEvent.click(nextBtn);

    // Verify dynamic question 2 is loaded
    await waitFor(() => {
      expect(screen.getByText(mockQuestion2.question)).toBeInTheDocument();
    });
  });
});
