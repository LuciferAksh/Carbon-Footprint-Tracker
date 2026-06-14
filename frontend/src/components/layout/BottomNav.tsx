/**
 * @fileoverview Bottom navigation component with 4 tabs.
 * Mobile-first with icon + label, active state highlighting.
 */
import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Home, PlusCircle, Trophy, User, MessageSquare } from 'lucide-react';

interface NavItem {
  path: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

const navItems: NavItem[] = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/log', label: 'Log', icon: PlusCircle },
  { path: '/coach', label: 'Coach', icon: MessageSquare },
  { path: '/challenges', label: 'Challenges', icon: Trophy },
  { path: '/profile', label: 'Profile', icon: User },
];

/**
 * Bottom navigation bar with 4 tabs: Home, Log, Challenges, Profile.
 * Uses Lucide icons with animated active indicator.
 */
const BottomNav = React.memo(function BottomNav() {
  const location = useLocation();

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-40 glass border-t border-dark-700/50 safe-bottom"
      aria-label="Main navigation"
    >
      <div className="flex items-center justify-around max-w-lg mx-auto h-16">
        {navItems.map((item) => {
          const isActive =
            item.path === '/' ? location.pathname === '/' : location.pathname.startsWith(item.path);
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className="relative flex flex-col items-center justify-center w-16 h-full group focus-visible:outline-none"
              aria-label={item.label}
              aria-current={isActive ? 'page' : undefined}
            >
              {isActive && (
                <motion.div
                  layoutId="nav-indicator"
                  className="absolute -top-px left-2 right-2 h-0.5 bg-primary-500 rounded-full"
                  transition={{ type: 'spring', stiffness: 500, damping: 35 }}
                />
              )}
              <Icon
                className={`w-5 h-5 transition-colors duration-200 ${
                  isActive ? 'text-primary-400' : 'text-dark-400 group-hover:text-dark-300'
                }`}
                aria-hidden="true"
              />
              <span
                className={`text-[10px] mt-1 font-medium transition-colors duration-200 ${
                  isActive ? 'text-primary-400' : 'text-dark-400 group-hover:text-dark-300'
                }`}
              >
                {item.label}
              </span>
              {/* Focus ring */}
              <span className="absolute inset-1 rounded-xl ring-0 group-focus-visible:ring-2 ring-primary-500" />
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
});

export default BottomNav;
