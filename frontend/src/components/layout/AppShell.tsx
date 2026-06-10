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
      {/* Ambient Moving Aurora Glows */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0" aria-hidden="true">
        {/* Sphere 1 */}
        <div className="absolute top-[-10%] left-[-15%] w-[70vw] h-[70vw] rounded-full bg-primary-500/8 blur-[100px] animate-aurora-slow" />
        {/* Sphere 2 */}
        <div className="absolute bottom-[10%] right-[-20%] w-[85vw] h-[85vw] rounded-full bg-primary-800/10 blur-[130px] animate-aurora-reverse" />
        {/* Radial green glow at top */}
        <div className="absolute inset-0 gradient-radial" />
      </div>

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
