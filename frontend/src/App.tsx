/**
 * @fileoverview Root application component with routing.
 * Uses React.lazy for route-level code splitting and Error Boundaries on every route.
 */
import { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '@/features/auth';
import ProtectedRoute from '@/features/auth/ProtectedRoute';
import { AppShell } from '@/components/layout';
import { ErrorBoundary } from '@/components/feedback';
import { LoadingSpinner } from '@/components/feedback';
import { useFocusOnRouteChange } from '@/lib/hooks/useFocusOnRouteChange';

/* Lazy-loaded route components for bundle splitting */
const LoginScreen = lazy(() => import('@/features/auth/LoginScreen'));
const OnboardingQuiz = lazy(() => import('@/features/onboarding/OnboardingQuiz'));
const DashboardScreen = lazy(() => import('@/features/dashboard/DashboardScreen'));
const LogScreen = lazy(() => import('@/features/activity-log/LogScreen'));
const ChallengesScreen = lazy(() => import('@/features/challenges/ChallengesScreen'));
const ChallengeDetail = lazy(() => import('@/features/challenges/ChallengeDetail'));
const MonthlyReport = lazy(() => import('@/features/reports/MonthlyReport'));
const ProfileScreen = lazy(() => import('@/features/profile/ProfileScreen'));
const CoachScreen = lazy(() => import('@/features/coach/CoachScreen'));

/**
 * Suspense fallback for lazy-loaded routes.
 */
function RouteFallback() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-dark-950" role="status">
      <LoadingSpinner size="lg" />
      <span className="sr-only">Loading page...</span>
    </div>
  );
}

/**
 * Root App component.
 * Defines all application routes with lazy loading and error boundaries.
 */
export default function App() {
  const { hasCompletedOnboarding, loading } = useAuth();
  useFocusOnRouteChange();

  if (loading) {
    return <RouteFallback />;
  }

  return (
    <Suspense fallback={<RouteFallback />}>
      <Routes>
        {/* Public route */}
        <Route
          path="/login"
          element={
            <ErrorBoundary>
              <LoginScreen />
            </ErrorBoundary>
          }
        />

        {/* Onboarding routes — must NOT require onboarding completion */}
        <Route
          path="/onboarding"
          element={
            <ProtectedRoute requireOnboarding={false}>
              <ErrorBoundary>
                <OnboardingQuiz />
              </ErrorBoundary>
            </ProtectedRoute>
          }
        />

        {/* Main app routes — wrapped in AppShell for bottom nav */}
        <Route
          element={
            <ProtectedRoute>
              <AppShell />
            </ProtectedRoute>
          }
        >
          <Route
            index
            element={
              hasCompletedOnboarding ? (
                <ErrorBoundary>
                  <DashboardScreen />
                </ErrorBoundary>
              ) : (
                <Navigate to="/onboarding" replace />
              )
            }
          />
          <Route
            path="log"
            element={
              <ErrorBoundary>
                <LogScreen />
              </ErrorBoundary>
            }
          />
          <Route
            path="challenges"
            element={
              <ErrorBoundary>
                <ChallengesScreen />
              </ErrorBoundary>
            }
          />
          <Route
            path="challenges/:id"
            element={
              <ErrorBoundary>
                <ChallengeDetail />
              </ErrorBoundary>
            }
          />
          <Route
            path="report"
            element={
              <ErrorBoundary>
                <MonthlyReport />
              </ErrorBoundary>
            }
          />
          <Route
            path="profile"
            element={
              <ErrorBoundary>
                <ProfileScreen />
              </ErrorBoundary>
            }
          />
          <Route
            path="coach"
            element={
              <ErrorBoundary>
                <CoachScreen />
              </ErrorBoundary>
            }
          />
        </Route>

        {/* Catch-all redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}
