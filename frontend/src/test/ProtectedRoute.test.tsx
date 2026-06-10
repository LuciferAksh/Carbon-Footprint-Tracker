import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from '../features/auth/ProtectedRoute';
import { useAuth } from '../features/auth/AuthProvider';

vi.mock('../features/auth/AuthProvider', () => ({
  useAuth: vi.fn(),
}));

describe('ProtectedRoute component', () => {
  it('redirects to login when unauthenticated', () => {
    (useAuth as any).mockReturnValue({
      user: null,
      loading: false,
      hasCompletedOnboarding: false,
    });

    render(
      <MemoryRouter initialEntries={['/protected']}>
        <Routes>
          <Route path="/login" element={<span>Login Screen</span>} />
          <Route
            path="/protected"
            element={
              <ProtectedRoute>
                <span>Protected Content</span>
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText('Login Screen')).toBeInTheDocument();
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });

  it('passes when authenticated and onboarding complete', () => {
    (useAuth as any).mockReturnValue({
      user: { uid: '123' },
      loading: false,
      hasCompletedOnboarding: true,
    });

    render(
      <MemoryRouter initialEntries={['/protected']}>
        <Routes>
          <Route
            path="/protected"
            element={
              <ProtectedRoute>
                <span>Protected Content</span>
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText('Protected Content')).toBeInTheDocument();
  });

  it('redirects to onboarding when profile incomplete', () => {
    (useAuth as any).mockReturnValue({
      user: { uid: '123' },
      loading: false,
      hasCompletedOnboarding: false,
    });

    render(
      <MemoryRouter initialEntries={['/protected']}>
        <Routes>
          <Route path="/onboarding" element={<span>Onboarding Quiz</span>} />
          <Route
            path="/protected"
            element={
              <ProtectedRoute>
                <span>Protected Content</span>
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText('Onboarding Quiz')).toBeInTheDocument();
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });
});
