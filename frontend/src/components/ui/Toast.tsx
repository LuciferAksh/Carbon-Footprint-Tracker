/**
 * @fileoverview Toast notification component with auto-dismiss and animations.
 */
import React, { useCallback, useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import type { ToastMessage } from '@/types';

interface ToastProviderProps {
  children: React.ReactNode;
}

interface ToastContextType {
  addToast: (toast: Omit<ToastMessage, 'id'>) => void;
  removeToast: (id: string) => void;
}

const ToastContext = React.createContext<ToastContextType | null>(null);

const iconMap = {
  success: CheckCircle,
  error: AlertCircle,
  warning: AlertTriangle,
  info: Info,
} as const;

const colorMap = {
  success: 'border-green-500/30 bg-green-500/10',
  error: 'border-red-500/30 bg-red-500/10',
  warning: 'border-amber-500/30 bg-amber-500/10',
  info: 'border-blue-500/30 bg-blue-500/10',
} as const;

const iconColorMap = {
  success: 'text-green-400',
  error: 'text-red-400',
  warning: 'text-amber-400',
  info: 'text-blue-400',
} as const;

/**
 * Individual toast notification item with auto-dismiss.
 */
const ToastItem = React.memo<{ toast: ToastMessage; onRemove: (id: string) => void }>(
  function ToastItem({ toast, onRemove }) {
    const Icon = iconMap[toast.type];

    useEffect(() => {
      const timer = setTimeout(() => {
        onRemove(toast.id);
      }, toast.duration || 5000);
      return () => clearTimeout(timer);
    }, [toast.id, toast.duration, onRemove]);

    return (
      <motion.div
        initial={{ opacity: 0, y: -20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: -20, scale: 0.95 }}
        className={`
          glass rounded-xl p-4 border shadow-xl max-w-sm w-full
          ${colorMap[toast.type]}
        `}
        role="alert"
        aria-live="assertive"
      >
        <div className="flex items-start gap-3">
          <Icon
            className={`w-5 h-5 shrink-0 mt-0.5 ${iconColorMap[toast.type]}`}
            aria-hidden="true"
          />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-dark-100">{toast.title}</p>
            <p className="text-xs text-dark-400 mt-0.5">{toast.message}</p>
          </div>
          <button
            onClick={() => onRemove(toast.id)}
            className="text-dark-400 hover:text-dark-200 transition-colors p-0.5 rounded"
            aria-label="Dismiss notification"
          >
            <X className="w-4 h-4" aria-hidden="true" />
          </button>
        </div>
      </motion.div>
    );
  },
);

/**
 * Toast provider component that manages toast notifications.
 * Wrap your app with this to enable toast notifications throughout.
 * @param props - Provider properties with children
 */
export function ToastProvider({ children }: ToastProviderProps) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = useCallback((toast: Omit<ToastMessage, 'id'>) => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
    setToasts((prev) => [...prev, { ...toast, id }]);
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ addToast, removeToast }}>
      {children}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-2" role="region" aria-label="Notifications">
        <AnimatePresence mode="sync">
          {toasts.map((toast) => (
            <ToastItem key={toast.id} toast={toast} onRemove={removeToast} />
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}

/**
 * Hook to access toast notifications.
 * @returns Object with addToast and removeToast methods.
 */
export function useToast(): ToastContextType {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}
