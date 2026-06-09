/**
 * @fileoverview Application entry point.
 * Initializes React with AuthProvider and BrowserRouter.
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from '@/features/auth';
import { ToastProvider } from '@/components/ui/Toast';
import './index.css';

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element not found. Ensure index.html has a div with id="root".');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider>
          <App />
        </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
