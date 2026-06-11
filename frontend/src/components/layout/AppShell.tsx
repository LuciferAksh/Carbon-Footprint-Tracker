/**
 * @fileoverview App shell layout component wrapping all authenticated pages.
 * Provides gradient background, scrollable content area, and bottom navigation.
 */
import React from 'react';
import { Outlet } from 'react-router-dom';
import BottomNav from './BottomNav';

/**
 * App shell layout with gradient radial background, scrollable main content,
 * and fixed bottom navigation. Bottom padding accounts for the nav bar.
 */
const AppShell = React.memo(function AppShell() {
  return (
    <div className="min-h-dvh flex flex-col gradient-dark relative overflow-hidden">
      {/* Skip navigation (WCAG 2.4.1) — visible only on keyboard focus */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:top-2 focus:left-2 focus:px-4 focus:py-2 focus:bg-primary-600 focus:text-white focus:rounded-md focus:outline-none"
      >
        Skip to main content
      </a>
      {/* Ambient Moving Aurora Glows */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0" aria-hidden="true">
        {/* Sphere 1 */}
        <div className="absolute top-[-10%] left-[-15%] w-[70vw] h-[70vw] rounded-full bg-primary-500/8 blur-[100px] animate-aurora-slow" />
        {/* Sphere 2 */}
        <div className="absolute bottom-[10%] right-[-20%] w-[85vw] h-[85vw] rounded-full bg-primary-800/10 blur-[130px] animate-aurora-reverse" />
        {/* Radial green glow at top */}
        <div className="absolute inset-0 gradient-radial" />
      </div>

      {/* Scrollable content area — child routes provide their own <main> landmark */}
      <div className="flex-1 relative z-10 pb-20 overflow-y-auto">
        <Outlet />
      </div>

      {/* Bottom navigation */}
      <BottomNav />
    </div>
  );
});

export default AppShell;
