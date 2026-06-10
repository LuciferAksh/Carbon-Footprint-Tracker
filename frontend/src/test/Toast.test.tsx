import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitForElementToBeRemoved } from '@testing-library/react';
import { ToastProvider, useToast } from '../components/ui/Toast';

function TestComponent() {
  const { addToast } = useToast();
  return (
    <button
      onClick={() => addToast({ type: 'success', title: 'Success Toast', message: 'It worked!' })}
    >
      Trigger Toast
    </button>
  );
}

describe('Toast component', () => {
  it('adds and removes toasts correctly', async () => {
    render(
      <ToastProvider>
        <TestComponent />
      </ToastProvider>,
    );

    const button = screen.getByRole('button', { name: /trigger toast/i });
    fireEvent.click(button);

    expect(screen.getByText('Success Toast')).toBeInTheDocument();
    expect(screen.getByText('It worked!')).toBeInTheDocument();

    const closeButton = screen.getByRole('button', { name: /dismiss notification/i });
    fireEvent.click(closeButton);

    await waitForElementToBeRemoved(() => screen.queryByText('Success Toast'));
  });
});
