/**
 * @fileoverview Stunning login screen with animated earth/leaf elements,
 * gradient background, and Google Sign-In.
 */
import React, { useCallback, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Leaf, Globe, Sprout, TreePine, Wind } from 'lucide-react';
import { useAuth } from './AuthProvider';
import Button from '@/components/ui/Button';

/** Floating particle type for background decoration */
interface FloatingParticle {
  id: number;
  icon: React.ComponentType<{ className?: string }>;
  x: number;
  y: number;
  size: number;
  duration: number;
  delay: number;
}

const particles: FloatingParticle[] = [
  { id: 1, icon: Leaf, x: 10, y: 20, size: 24, duration: 8, delay: 0 },
  { id: 2, icon: Sprout, x: 80, y: 15, size: 20, duration: 10, delay: 1 },
  { id: 3, icon: TreePine, x: 15, y: 70, size: 28, duration: 12, delay: 2 },
  { id: 4, icon: Wind, x: 75, y: 65, size: 22, duration: 9, delay: 0.5 },
  { id: 5, icon: Leaf, x: 50, y: 85, size: 18, duration: 11, delay: 1.5 },
  { id: 6, icon: Sprout, x: 90, y: 45, size: 16, duration: 7, delay: 3 },
  { id: 7, icon: Leaf, x: 30, y: 40, size: 14, duration: 13, delay: 2.5 },
  { id: 8, icon: Wind, x: 60, y: 30, size: 20, duration: 8, delay: 4 },
];

/**
 * Login screen with stunning animated background, floating nature elements,
 * and Google Sign-In button. Redirects to home if already authenticated.
 */
const LoginScreen = React.memo(function LoginScreen() {
  const { user, signInWithGoogle, signInAsDemo, isDemoMode, loading, hasCompletedOnboarding } = useAuth();
  const [signingIn, setSigningIn] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGoogleSignIn = useCallback(async () => {
    try {
      setSigningIn(true);
      setError(null);
      await signInWithGoogle();
    } catch {
      setError('Sign in failed. Please try again.');
    } finally {
      setSigningIn(false);
    }
  }, [signInWithGoogle]);

  const handleDemoSignIn = useCallback(() => {
    signInAsDemo();
  }, [signInAsDemo]);

  // Redirect if already authenticated
  if (user && !loading) {
    return <Navigate to={hasCompletedOnboarding ? '/' : '/onboarding'} replace />;
  }

  return (
    <div className="min-h-dvh relative overflow-hidden flex flex-col items-center justify-center px-6">
      {/* Animated gradient background */}
      <div
        className="absolute inset-0 bg-gradient-to-br from-dark-950 via-dark-900 to-primary-950"
        aria-hidden="true"
      />

      {/* Radial glow effects */}
      <div
        className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-primary-600/10 blur-3xl"
        aria-hidden="true"
      />
      <div
        className="absolute bottom-0 left-0 w-[400px] h-[400px] rounded-full bg-primary-700/5 blur-3xl"
        aria-hidden="true"
      />

      {/* Floating particles */}
      {particles.map((particle) => {
        const Icon = particle.icon;
        return (
          <motion.div
            key={particle.id}
            className="absolute text-primary-500/20"
            style={{ left: `${particle.x}%`, top: `${particle.y}%` }}
            animate={{
              y: [-20, 20, -20],
              x: [-10, 10, -10],
              rotate: [0, 180, 360],
              opacity: [0.1, 0.3, 0.1],
            }}
            transition={{
              duration: particle.duration,
              repeat: Infinity,
              delay: particle.delay,
              ease: 'easeInOut',
            }}
            aria-hidden="true"
          >
            <Icon className={`w-[${particle.size}px] h-[${particle.size}px]`} />
          </motion.div>
        );
      })}

      {/* Main content */}
      <motion.div
        className="relative z-10 text-center max-w-sm w-full space-y-8"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
      >
        {/* Logo / Earth icon */}
        <motion.div
          className="mx-auto w-24 h-24 rounded-full gradient-primary flex items-center justify-center shadow-2xl shadow-primary-600/30"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
        >
          <Globe className="w-12 h-12 text-white" aria-hidden="true" />
        </motion.div>

        {/* App name and tagline */}
        <div className="space-y-3">
          <motion.h1
            className="text-4xl font-bold"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
          >
            <span className="text-dark-100">Carbon</span>
            <span className="text-primary-400">Coach</span>
          </motion.h1>
          <motion.p
            className="text-dark-400 text-lg leading-relaxed"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            Track your carbon footprint.
            <br />
            <span className="text-primary-400/80">Save the planet.</span>
          </motion.p>
        </div>

        {/* Feature badges */}
        <motion.div
          className="flex justify-center gap-3 flex-wrap"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7, duration: 0.6 }}
        >
          {['AI-Powered', 'Real-time Tracking', 'Challenges'].map((feature) => (
            <span
              key={feature}
              className="px-3 py-1.5 rounded-full text-xs font-medium bg-primary-600/10 text-primary-400 border border-primary-600/20"
            >
              {feature}
            </span>
          ))}
        </motion.div>

        {/* Sign in buttons */}
        <motion.div
          className="space-y-4 pt-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9, duration: 0.6 }}
        >
          {/* Demo Mode Login — shown when VITE_DEMO_MODE=true */}
          {isDemoMode && (
            <>
              <Button
                onClick={handleDemoSignIn}
                fullWidth
                size="lg"
                className="relative overflow-hidden"
                aria-label="Explore CarbonCoach as a demo user"
                icon={<Leaf className="w-5 h-5" />}
              >
                Explore as Demo User
              </Button>

              <div className="flex items-center gap-3 px-2">
                <div className="flex-1 h-px bg-dark-700" />
                <span className="text-xs text-dark-500">or</span>
                <div className="flex-1 h-px bg-dark-700" />
              </div>
            </>
          )}

          {/* Google Sign-In */}
          <Button
            onClick={handleGoogleSignIn}
            loading={signingIn}
            fullWidth
            size="lg"
            variant={isDemoMode ? 'secondary' : undefined}
            className="relative overflow-hidden"
            aria-label="Sign in with Google account"
            icon={
              <svg className="w-5 h-5" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
                  fill="#4285F4"
                />
                <path
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  fill="#34A853"
                />
                <path
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  fill="#FBBC05"
                />
                <path
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  fill="#EA4335"
                />
              </svg>
            }
          >
            Continue with Google
          </Button>

          {isDemoMode && (
            <p className="text-xs text-primary-600/60 text-center">
              🧪 Demo Mode — no Firebase project needed
            </p>
          )}

          {error && (
            <motion.p
              className="text-sm text-error text-center"
              role="alert"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {error}
            </motion.p>
          )}

          <p className="text-xs text-dark-500 text-center">
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
        </motion.div>
      </motion.div>

      {/* Bottom gradient fade */}
      <div
        className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-dark-950 to-transparent"
        aria-hidden="true"
      />
    </div>
  );
});

export default LoginScreen;
