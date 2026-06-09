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
    <div className="min-h-dvh flex flex-col gradient-dark">
      {/* Radial green glow at top */}
      <div className="fixed inset-0 gradient-radial pointer-events-none" aria-hidden="true" />

      {/* Main scrollable content */}
      <main className="flex-1 relative z-10 pb-20 overflow-y-auto">
        <Outlet />
      </main>

      {/* Bottom navigation */}
      <BottomNav />
    </div>
  );
});

export default AppShell;
