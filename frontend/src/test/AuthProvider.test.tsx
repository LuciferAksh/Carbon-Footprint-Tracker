import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { AuthProvider, useAuth } from '../features/auth/AuthProvider';

vi.mock('../lib/api', () => ({
  api: {
    get: vi.fn().mockResolvedValue({ data: { uid: 'demo-user-001', onboardingComplete: true } }),
    post: vi.fn().mockResolvedValue({ data: {} }),
  },
}));

vi.mock('../lib/firebase', () => ({
  auth: {
    currentUser: null,
  },
  googleProvider: {},
}));

vi.mock('firebase/auth', () => ({
  onAuthStateChanged: vi.fn().mockImplementation((_auth, callback) => {
    callback(null);
    return () => {};
  }),
  signInWithPopup: vi.fn(),
  signOut: vi.fn(),
}));

function AuthConsumer() {
  const { user, signInAsDemo, signOut, hasCompletedOnboarding } = useAuth();
  return (
    <div>
      <span data-testid="user">{user ? user.displayName : 'anonymous'}</span>
      <span data-testid="onboarding">{hasCompletedOnboarding ? 'done' : 'pending'}</span>
      <button onClick={signInAsDemo}>Sign In Demo</button>
      <button onClick={signOut}>Sign Out</button>
    </div>
  );
}

describe('AuthProvider component', () => {
  it('renders default anonymous state', () => {
    render(
      <AuthProvider>
        <AuthConsumer />
      </AuthProvider>,
    );
    expect(screen.getByTestId('user')).toHaveTextContent('anonymous');
    expect(screen.getByTestId('onboarding')).toHaveTextContent('pending');
  });

  it('signs in as demo user correctly', () => {
    render(
      <AuthProvider>
        <AuthConsumer />
      </AuthProvider>,
    );
    const btn = screen.getByRole('button', { name: /sign in demo/i });
    act(() => {
      btn.click();
    });
    expect(screen.getByTestId('user')).toHaveTextContent('Demo User');
  });
});
