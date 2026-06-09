/**
 * @fileoverview Firebase configuration and initialization.
 * Reads configuration from VITE_FIREBASE_* environment variables.
 * In demo mode, Firebase is still initialized but never actually used for auth.
 */
import { initializeApp, type FirebaseApp } from 'firebase/app';
import { getAuth, type Auth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'demo-key',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'demo.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'demo-project',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'demo.appspot.com',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '000000000000',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:000:web:demo',
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || '',
};

/** Firebase app instance */
export const app: FirebaseApp = initializeApp(firebaseConfig);

/** Firebase auth instance */
export const auth: Auth = getAuth(app);

/** Google auth provider for sign-in */
export const googleProvider = new GoogleAuthProvider();
