/**
 * @fileoverview Authentication context provider and hook.
 * Manages Firebase auth state, user profile, and loading states.
 * Supports DEMO MODE for local development without a real Firebase project.
 */
import React, { createContext, useCallback, useEffect, useState } from 'react';
import {
  onAuthStateChanged,
  signInWithPopup,
  signOut as firebaseSignOut,
  type User,
} from 'firebase/auth';
import { auth, googleProvider } from '@/lib/firebase';
import type { UserProfile } from '@/types';
import { api } from '@/lib/api';

/** Whether demo mode is active (no real Firebase needed) */
const IS_DEMO_MODE = import.meta.env.VITE_DEMO_MODE === 'true';

/** Mock user for demo mode */
const DEMO_USER = {
  uid: 'demo-user-001',
  email: 'demo@carboncoach.dev',
  displayName: 'Demo User',
  photoURL: null,
  emailVerified: true,
  getIdToken: async () => 'demo-token',
} as unknown as User;

/** Mock profile for demo mode */
const DEMO_PROFILE: UserProfile = {
  uid: 'demo-user-001',
  email: 'demo@carboncoach.dev',
  displayName: 'Demo User',
  photoURL: null,
  onboardingComplete: false,
  createdAt: new Date().toISOString(),
};

interface AuthContextType {
  /** Current Firebase user (or demo user) */
  user: User | null;
  /** User profile from backend */
  profile: UserProfile | null;
  /** Whether auth is being checked */
  loading: boolean;
  /** Whether the user has completed onboarding */
  hasCompletedOnboarding: boolean;
  /** Whether demo mode is active */
  isDemoMode: boolean;
  /** Sign in with Google */
  signInWithGoogle: () => Promise<void>;
  /** Sign in as demo user (local dev only) */
  signInAsDemo: () => void;
  /** Sign out */
  signOut: () => Promise<void>;
  /** Refresh user profile from backend */
  refreshProfile: () => Promise<void>;
  /** Set onboarding as complete */
  setOnboardingComplete: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

/**
 * Authentication provider component.
 * Wraps the app to provide auth state and methods throughout the component tree.
 * When VITE_DEMO_MODE=true, Firebase calls are bypassed entirely.
 * @param props - Provider properties with children
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [hasCompletedOnboarding, setHasCompletedOnboarding] = useState(false);

  const refreshProfile = useCallback(async () => {
    if (IS_DEMO_MODE) {
      // In demo mode, just use the local profile state
      return;
    }
    try {
      const response = await api.get<UserProfile>('/users/me');
      setProfile(response.data);
      setHasCompletedOnboarding(response.data.onboardingComplete);
    } catch {
      // Profile may not exist yet (new user)
      setProfile(null);
      setHasCompletedOnboarding(false);
    }
  }, []);

  useEffect(() => {
    if (IS_DEMO_MODE) {
      // In demo mode, check localStorage for persisted demo session
      const savedDemo = localStorage.getItem('carboncoach_demo_session');
      if (savedDemo) {
        const saved = JSON.parse(savedDemo) as { onboardingComplete: boolean };
        setUser(DEMO_USER);
        setProfile({ ...DEMO_PROFILE, onboardingComplete: saved.onboardingComplete });
        setHasCompletedOnboarding(saved.onboardingComplete);
      }
      setLoading(false);
      return;
    }

    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      setUser(firebaseUser);
      if (firebaseUser) {
        await refreshProfile();
      } else {
        setProfile(null);
        setHasCompletedOnboarding(false);
      }
      setLoading(false);
    });

    return unsubscribe;
  }, [refreshProfile]);

  /** Sign in as demo user — no Firebase needed */
  const signInAsDemo = useCallback(() => {
    setUser(DEMO_USER);
    setProfile({ ...DEMO_PROFILE });
    setHasCompletedOnboarding(false);
    localStorage.setItem('carboncoach_demo_session', JSON.stringify({ onboardingComplete: false }));
  }, []);

  const signInWithGoogle = useCallback(async () => {
    if (IS_DEMO_MODE) {
      signInAsDemo();
      return;
    }
    try {
      setLoading(true);
      await signInWithPopup(auth, googleProvider);
    } catch (error) {
      console.error('Google sign-in failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [signInAsDemo]);

  const signOut = useCallback(async () => {
    if (IS_DEMO_MODE) {
      setUser(null);
      setProfile(null);
      setHasCompletedOnboarding(false);
      localStorage.removeItem('carboncoach_demo_session');
      return;
    }
    try {
      await firebaseSignOut(auth);
      setProfile(null);
      setHasCompletedOnboarding(false);
    } catch (error) {
      console.error('Sign out failed:', error);
      throw error;
    }
  }, []);

  const setOnboardingComplete = useCallback(() => {
    setHasCompletedOnboarding(true);
    if (profile) {
      setProfile({ ...profile, onboardingComplete: true });
    }
    if (IS_DEMO_MODE) {
      localStorage.setItem('carboncoach_demo_session', JSON.stringify({ onboardingComplete: true }));
    }
  }, [profile]);

  const value: AuthContextType = {
    user,
    profile,
    loading,
    hasCompletedOnboarding,
    isDemoMode: IS_DEMO_MODE,
    signInWithGoogle,
    signInAsDemo,
    signOut,
    refreshProfile,
    setOnboardingComplete,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to access authentication context.
 * Must be used within an AuthProvider.
 * @returns Auth context with user, profile, and auth methods.
 * @throws Error if used outside AuthProvider.
 */
export function useAuth(): AuthContextType {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
