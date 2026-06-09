/**
 * @fileoverview Protected route component that requires authentication.
 * Redirects to login if not authenticated, to onboarding if profile incomplete.
 */
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthProvider';
import LoadingSpinner from '@/components/feedback/LoadingSpinner';

interface ProtectedRouteProps {
  /** Child components to render when authenticated */
  children: React.ReactNode;
  /** Whether onboarding completion is required */
  requireOnboarding?: boolean;
}

/**
 * Route guard that checks authentication and onboarding status.
 * Redirects unauthenticated users to /login and users without profiles to /onboarding.
 * @param props - ProtectedRoute properties
 */
const ProtectedRoute = React.memo<ProtectedRouteProps>(function ProtectedRoute({
  children,
  requireOnboarding = true,
}) {
  const { user, loading, hasCompletedOnboarding } = useAuth();
  const location = useLocation();

  if (loading) {
    return <LoadingSpinner fullScreen message="Checking authentication..." />;
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requireOnboarding && !hasCompletedOnboarding) {
    return <Navigate to="/onboarding" replace />;
  }

  return <>{children}</>;
});

export default ProtectedRoute;
