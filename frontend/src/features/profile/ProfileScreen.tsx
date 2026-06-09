/**
 * @fileoverview Profile screen with user info, carbon score history,
 * streak, badges, and settings.
 */
import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { User, LogOut, Award, Flame, Leaf, Settings, Bell, ChevronRight } from 'lucide-react';
import { Card, Badge, Button } from '@/components/ui';
import { useAuth } from '@/features/auth';

/** Badge definitions based on achievements */
const ACHIEVEMENT_BADGES = [
  { id: 'first-log', label: 'First Log', emoji: '🌱', desc: 'Logged your first activity', earned: true },
  { id: 'week-streak', label: '7-Day Streak', emoji: '🔥', desc: '7 consecutive days logged', earned: true },
  { id: 'challenge-1', label: 'Challenger', emoji: '🏆', desc: 'Completed first challenge', earned: true },
  { id: 'green-commute', label: 'Green Commuter', emoji: '🚇', desc: 'Took public transport 10 times', earned: true },
  { id: 'vegan-week', label: 'Vegan Warrior', emoji: '🥗', desc: '7 vegan meals in a week', earned: false },
  { id: 'carbon-a', label: 'A-Score', emoji: '⭐', desc: 'Reached Carbon Score A', earned: false },
] as const;

/**
 * Profile screen component.
 */
export default function ProfileScreen() {
  const { user, profile, signOut } = useAuth();

  const earnedBadges = useMemo(() => ACHIEVEMENT_BADGES.filter(b => b.earned), []);
  const lockedBadges = useMemo(() => ACHIEVEMENT_BADGES.filter(b => !b.earned), []);

  return (
    <main id="main-content" className="px-4 pt-6 pb-24 max-w-lg mx-auto" role="main">
      {/* Profile Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <Card className="p-6 mb-4 text-center">
          {/* Avatar */}
          <div className="w-20 h-20 rounded-full mx-auto mb-3 overflow-hidden border-2 border-primary-600/50">
            {user?.photoURL ? (
              <img
                src={user.photoURL}
                alt={`${user.displayName || 'User'}'s avatar`}
                className="w-full h-full object-cover"
                referrerPolicy="no-referrer"
              />
            ) : (
              <div className="w-full h-full bg-dark-700 flex items-center justify-center">
                <User size={32} className="text-dark-400" aria-hidden="true" />
              </div>
            )}
          </div>

          <h1 className="text-xl font-bold text-white">{user?.displayName || 'CarbonCoach User'}</h1>
          <p className="text-sm text-dark-400">{user?.email}</p>

          {/* Carbon Profile Type */}
            {profile?.onboardingComplete && (
              <Badge variant="primary" className="mt-3 text-sm">
                <Leaf size={14} className="mr-1" aria-hidden="true" />
                The Urban Commuter
              </Badge>
            )}
        </Card>
      </motion.div>

      {/* Stats Row */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <div className="grid grid-cols-3 gap-3 mb-4">
          <Card className="p-3 text-center">
            <Flame size={20} className="text-orange-400 mx-auto mb-1" aria-hidden="true" />
            <p className="text-xl font-bold text-white">7</p>
            <p className="text-xs text-dark-400">Day Streak</p>
          </Card>
          <Card className="p-3 text-center">
            <Award size={20} className="text-primary-400 mx-auto mb-1" aria-hidden="true" />
            <p className="text-xl font-bold text-primary-400">B</p>
            <p className="text-xs text-dark-400">Carbon Score</p>
          </Card>
          <Card className="p-3 text-center">
            <Leaf size={20} className="text-green-400 mx-auto mb-1" aria-hidden="true" />
            <p className="text-xl font-bold text-white">{earnedBadges.length}</p>
            <p className="text-xs text-dark-400">Badges</p>
          </Card>
        </div>
      </motion.div>

      {/* Earned Badges */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <Card className="p-5 mb-4">
          <h2 className="text-sm font-semibold text-dark-300 mb-3">🏅 Earned Badges</h2>
          <div className="grid grid-cols-2 gap-2">
            {earnedBadges.map((badge) => (
              <div
                key={badge.id}
                className="flex items-center gap-3 p-3 rounded-xl bg-dark-800/50 border border-primary-800/20"
              >
                <span className="text-2xl" role="img" aria-label={badge.label}>{badge.emoji}</span>
                <div>
                  <p className="text-sm font-medium text-white">{badge.label}</p>
                  <p className="text-xs text-dark-400">{badge.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </motion.div>

      {/* Locked Badges */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
        <Card className="p-5 mb-4">
          <h2 className="text-sm font-semibold text-dark-300 mb-3">🔒 Locked Badges</h2>
          <div className="grid grid-cols-2 gap-2">
            {lockedBadges.map((badge) => (
              <div
                key={badge.id}
                className="flex items-center gap-3 p-3 rounded-xl bg-dark-800/30 opacity-50"
              >
                <span className="text-2xl grayscale" role="img" aria-label={badge.label}>{badge.emoji}</span>
                <div>
                  <p className="text-sm font-medium text-dark-300">{badge.label}</p>
                  <p className="text-xs text-dark-500">{badge.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </motion.div>

      {/* Settings */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
        <Card className="p-4 mb-4">
          <h2 className="text-sm font-semibold text-dark-300 mb-3">
            <Settings size={16} className="inline mr-1" aria-hidden="true" />
            Settings
          </h2>
          <div className="space-y-1">
            <button
              className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-dark-800/50 transition-colors"
              type="button"
              aria-label="Notification settings"
            >
              <span className="flex items-center gap-2 text-sm text-dark-200">
                <Bell size={16} className="text-dark-400" aria-hidden="true" />
                Notifications
              </span>
              <ChevronRight size={16} className="text-dark-500" aria-hidden="true" />
            </button>
          </div>
        </Card>
      </motion.div>

      {/* Sign Out */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}>
        <Button
          variant="ghost"
          className="w-full text-red-400 hover:text-red-300 hover:bg-red-900/20"
          onClick={signOut}
          aria-label="Sign out of CarbonCoach"
        >
          <LogOut size={16} className="mr-2" aria-hidden="true" />
          Sign Out
        </Button>
      </motion.div>
    </main>
  );
}
