/**
 * @fileoverview Dashboard screen — "My Carbon Story".
 * Shows weekly CO2 comparison, category breakdown, community benchmark,
 * streak counter, carbon score badge, and current challenge preview.
 */
import { useState, useEffect, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Flame, Award, Users, TrendingDown, TrendingUp, Target, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Skeleton } from '@/components/ui';
import { BarChart } from '@/components/charts';
import { DonutChart } from '@/components/charts';
import { useAuth } from '@/features/auth';
import { api } from '@/lib/api';
import { CATEGORY_COLORS } from '@/lib/carbon-constants';
import type { DashboardData, Challenge } from '@/types';

/** Animated count-up hook */
function useCountUp(target: number, duration = 1500): number {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (target === 0) { setCount(0); return; }
    const startTime = performance.now();
    let animationFrame: number;

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      setCount(target * eased);
      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [target, duration]);

  return count;
}

/** Carbon Score letter grade */
function getCarbonGrade(score: number): { grade: string; color: string } {
  if (score >= 90) return { grade: 'A+', color: '#22c55e' };
  if (score >= 80) return { grade: 'A', color: '#4ade80' };
  if (score >= 70) return { grade: 'B', color: '#86efac' };
  if (score >= 60) return { grade: 'C', color: '#f59e0b' };
  return { grade: 'D', color: '#ef4444' };
}

/** Mock dashboard data for demo */
const MOCK_DASHBOARD: DashboardData = {
  totalCO2Today: 3.2,
  totalCO2Week: 24.8,
  totalCO2Month: 98.5,
  weeklyComparison: [
    { day: 'Mon', thisWeek: 4.2, lastWeek: 5.1 },
    { day: 'Tue', thisWeek: 3.8, lastWeek: 4.3 },
    { day: 'Wed', thisWeek: 2.9, lastWeek: 4.8 },
    { day: 'Thu', thisWeek: 5.1, lastWeek: 3.9 },
    { day: 'Fri', thisWeek: 3.5, lastWeek: 5.2 },
    { day: 'Sat', thisWeek: 2.8, lastWeek: 4.1 },
    { day: 'Sun', thisWeek: 2.5, lastWeek: 3.6 },
  ],
  categoryBreakdown: [
    { category: 'transport', amount: 9.8, percentage: 39.5, color: CATEGORY_COLORS.transport },
    { category: 'food', amount: 7.2, percentage: 29.0, color: CATEGORY_COLORS.food },
    { category: 'energy', amount: 5.3, percentage: 21.4, color: CATEGORY_COLORS.energy },
    { category: 'shopping', amount: 2.5, percentage: 10.1, color: CATEGORY_COLORS.shopping },
  ],
  streak: 7,
  carbonScore: 78,
  benchmark: { user: 24.8, national: 38.5, target: 20.0 },
};

const MOCK_CHALLENGE: Challenge = {
  id: '2026-W23',
  title: 'Metro Week Challenge',
  description: 'Take public transport at least 3 times this week instead of your car.',
  category: 'transport',
  difficulty: 'medium',
  durationDays: 7,
  co2SavedTarget: 4.2,
  co2SavedActual: 1.8,
  progress: 43,
  status: 'active',
  participants: 234,
  tips: [],
};

/**
 * Dashboard screen component.
 */
export default function DashboardScreen() {
  useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [challenge, setChallenge] = useState<Challenge | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        const [dashRes, chalRes] = await Promise.allSettled([
          api.get<DashboardData>('/activity/summary?period=week'),
          api.get<Challenge>('/challenge/current'),
        ]);
        setData(dashRes.status === 'fulfilled' ? dashRes.value.data : MOCK_DASHBOARD);
        setChallenge(chalRes.status === 'fulfilled' ? chalRes.value.data : MOCK_CHALLENGE);
      } catch {
        setData(MOCK_DASHBOARD);
        setChallenge(MOCK_CHALLENGE);
      } finally {
        setLoading(false);
      }
    }
    fetchDashboard();
  }, []);

  const weeklyTotal = useCountUp(data?.totalCO2Week ?? 0);
  const gradeInfo = useMemo(() => getCarbonGrade(data?.carbonScore ?? 0), [data?.carbonScore]);

  const weekChange = useMemo(() => {
    if (!data) return 0;
    const lastWeekTotal = data.weeklyComparison.reduce((sum, d) => sum + d.lastWeek, 0);
    if (lastWeekTotal === 0) return 0;
    return ((data.totalCO2Week - lastWeekTotal) / lastWeekTotal) * 100;
  }, [data]);

  if (loading) {
    return (
      <div className="px-4 pt-6 pb-24 max-w-lg mx-auto space-y-4" role="status">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-40 w-full rounded-2xl" />
        <Skeleton className="h-64 w-full rounded-2xl" />
        <span className="sr-only">Loading dashboard...</span>
      </div>
    );
  }

  return (
    <main id="main-content" className="px-4 pt-6 pb-24 max-w-lg mx-auto" role="main">
      {/* Header */}
      <header className="mb-6">
        <p className="text-dark-400 text-sm">Welcome back,</p>
        <h1 className="text-2xl font-bold text-white">My Carbon Story 🌍</h1>
      </header>

      {/* Hero CO2 Counter */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="p-6 mb-4 text-center glass-primary animate-pulse-glow">
          <p className="text-dark-300 text-sm mb-1">This Week's Footprint</p>
          <div className="flex items-baseline justify-center gap-1" aria-live="polite">
            <span className="text-5xl font-bold text-primary-400 tabular-nums">
              {weeklyTotal.toFixed(1)}
            </span>
            <span className="text-lg text-dark-400">kg CO₂</span>
          </div>
          <div className="flex items-center justify-center gap-1 mt-2">
            {weekChange <= 0 ? (
              <TrendingDown size={16} className="text-green-400" aria-hidden="true" />
            ) : (
              <TrendingUp size={16} className="text-red-400" aria-hidden="true" />
            )}
            <span className={`text-sm font-medium ${weekChange <= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {Math.abs(weekChange).toFixed(1)}% vs last week
            </span>
          </div>
        </Card>
      </motion.div>

      {/* Stats Row */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        {/* Streak */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <Card className="p-3 text-center">
            <Flame size={20} className="text-orange-400 mx-auto mb-1" aria-hidden="true" />
            <p className="text-xl font-bold text-white">{data?.streak ?? 0}</p>
            <p className="text-xs text-dark-400">Day Streak</p>
          </Card>
        </motion.div>

        {/* Carbon Score */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <Card className="p-3 text-center">
            <Award size={20} style={{ color: gradeInfo.color }} className="mx-auto mb-1" aria-hidden="true" />
            <p className="text-xl font-bold" style={{ color: gradeInfo.color }}>{gradeInfo.grade}</p>
            <p className="text-xs text-dark-400">Carbon Score</p>
          </Card>
        </motion.div>

        {/* Today */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Card className="p-3 text-center">
            <Target size={20} className="text-primary-400 mx-auto mb-1" aria-hidden="true" />
            <p className="text-xl font-bold text-white">{data?.totalCO2Today?.toFixed(1)}</p>
            <p className="text-xs text-dark-400">kg Today</p>
          </Card>
        </motion.div>
      </div>

      {/* Weekly Comparison Chart */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
        <Card className="p-4 mb-4">
          <h2 className="text-sm font-semibold text-dark-300 mb-3">This Week vs Last Week</h2>
          <BarChart data={data?.weeklyComparison ?? []} aria-label="Weekly CO2 comparison bar chart" />
        </Card>
      </motion.div>

      {/* Category Breakdown */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}>
        <Card className="p-4 mb-4">
          <h2 className="text-sm font-semibold text-dark-300 mb-3">Breakdown by Category</h2>
          <DonutChart data={data?.categoryBreakdown ?? []} aria-label="CO2 breakdown by category donut chart" />
        </Card>
      </motion.div>

      {/* Community Benchmark */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }}>
        <Card className="p-4 mb-4 glass-primary">
          <div className="flex items-center gap-2 mb-3">
            <Users size={18} className="text-primary-400" aria-hidden="true" />
            <h2 className="text-sm font-semibold text-dark-300">People Like You</h2>
          </div>
          {data?.benchmark && (
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs text-dark-400 mb-1">
                  <span>Your footprint</span>
                  <span>{data.benchmark.user.toFixed(1)} kg/week</span>
                </div>
                <div className="h-2 bg-dark-800 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min((data.benchmark.user / data.benchmark.national) * 100, 100)}%` }}
                    transition={{ duration: 1, delay: 0.8 }}
                    className="h-full bg-primary-500 rounded-full"
                  />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs text-dark-400 mb-1">
                  <span>National average</span>
                  <span>{data.benchmark.national.toFixed(1)} kg/week</span>
                </div>
                <div className="h-2 bg-dark-800 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '100%' }}
                    transition={{ duration: 1, delay: 0.9 }}
                    className="h-full bg-dark-500 rounded-full"
                  />
                </div>
              </div>
              <p className="text-sm font-medium text-primary-400 mt-2">
                🎉 You emit {((1 - data.benchmark.user / data.benchmark.national) * 100).toFixed(0)}% less than the national average!
              </p>
            </div>
          )}
        </Card>
      </motion.div>

      {/* Challenge Preview */}
      {challenge && challenge.status === 'active' && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }}>
          <button
            onClick={() => navigate(`/challenges/${challenge.id}`)}
            className="w-full text-left"
            aria-label={`View challenge: ${challenge.title}`}
            type="button"
          >
            <Card className="p-4 mb-4 border-primary-700/30 hover:border-primary-600/50 transition-colors">
              <div className="flex items-center justify-between mb-2">
                <Badge variant="primary">This Week's Mission</Badge>
                <ChevronRight size={18} className="text-dark-400" aria-hidden="true" />
              </div>
              <h3 className="text-base font-semibold text-white mb-1">{challenge.title}</h3>
              <p className="text-sm text-dark-400 mb-3">{challenge.description}</p>
              <div className="flex items-center gap-3">
                <div className="flex-1 h-2 bg-dark-800 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${challenge.progress}%` }}
                    transition={{ duration: 1, delay: 1 }}
                    className="h-full bg-primary-500 rounded-full"
                  />
                </div>
                <span className="text-xs text-dark-400 whitespace-nowrap">{challenge.progress}%</span>
              </div>
              <p className="text-xs text-primary-500 mt-2">
                🌱 Save {challenge.co2SavedTarget.toFixed(1)} kg CO₂ this week
              </p>
            </Card>
          </button>
        </motion.div>
      )}
    </main>
  );
}
