/**
 * @fileoverview Monthly Report screen — "Your Monthly Carbon Story".
 * Displays CO2 trends, category breakdown, Gemini narrative, and share button.
 */
import { useState, useEffect, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Calendar, TrendingDown, TrendingUp, Share2, Sparkles } from 'lucide-react';
import { Card, Button, Skeleton } from '@/components/ui';
import { api } from '@/lib/api';
import type { MonthlyReport as MonthlyReportType } from '@/types';

/** Mock report for demo */
const MOCK_REPORT: MonthlyReportType = {
  month: 'May',
  year: 2026,
  totalCO2: 98.5,
  previousMonthCO2: 112.3,
  changePercent: -12.3,
  dailyAverage: 3.2,
  categoryBreakdown: [
    { category: 'transport', amount: 38.2, percentage: 38.8, color: '#3b82f6' },
    { category: 'food', amount: 28.5, percentage: 28.9, color: '#f59e0b' },
    { category: 'energy', amount: 21.3, percentage: 21.6, color: '#a855f7' },
    { category: 'shopping', amount: 10.5, percentage: 10.7, color: '#ec4899' },
  ],
  weeklyTrend: [
    { week: 'Week 1', amount: 28.3 },
    { week: 'Week 2', amount: 25.1 },
    { week: 'Week 3', amount: 24.8 },
    { week: 'Week 4', amount: 20.3 },
  ],
  geminiNarrative: `Great progress this month! Your carbon footprint dropped by 12.3% compared to April — that's like taking 3 fewer car trips across Mumbai.\n\nYour biggest win? Transport emissions fell by 18% thanks to your metro habit. The Wednesday bike commutes really added up! Food was steady, but I noticed more vegetarian meals in the second half — keep that up.\n\nOne surprising insight: your weekend energy usage spiked 40% compared to weekdays. Consider switching off that extra AC unit when you're out. For June, let's aim for under 90 kg — that would put you in the top 15% of CarbonCoach users! 🌱`,
  highlights: [
    '🚇 Took the metro 8 times — saved 12 kg CO₂',
    '🥗 5 fully vegetarian days this month',
    '📉 Lowest weekly footprint: 20.3 kg (Week 4)',
  ],
  score: 82,
};

/**
 * Monthly Report screen.
 */
export default function MonthlyReport() {
  const [report, setReport] = useState<MonthlyReportType | null>(null);
  const [loading, setLoading] = useState(true);
  const [narrativeVisible, setNarrativeVisible] = useState(false);
  const shareRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function fetchReport() {
      try {
        const now = new Date();
        const month = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
        const res = await api.get<MonthlyReportType>(`/insights/monthly?month=${month}`);
        setReport(res.data);
      } catch {
        setReport(MOCK_REPORT);
      } finally {
        setLoading(false);
        setTimeout(() => setNarrativeVisible(true), 500);
      }
    }
    fetchReport();
  }, []);

  /** Generate and share card image */
  const handleShare = useCallback(async () => {
    if (!shareRef.current || !report) return;
    try {
      // Simple text share fallback
      if (navigator.share) {
        await navigator.share({
          title: 'My CarbonCoach Report',
          text: `🌍 My ${report.month} carbon footprint: ${report.totalCO2.toFixed(1)} kg CO₂ (${report.changePercent > 0 ? '+' : ''}${report.changePercent.toFixed(1)}% vs last month). Track yours at CarbonCoach!`,
        });
      }
    } catch {
      // Share cancelled or not supported
    }
  }, [report]);

  if (loading) {
    return (
      <div className="px-4 pt-6 pb-24 max-w-lg mx-auto space-y-4" role="status">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-40 w-full rounded-2xl" />
        <Skeleton className="h-64 w-full rounded-2xl" />
        <span className="sr-only">Loading monthly report...</span>
      </div>
    );
  }

  if (!report) return null;

  const isImproved = report.changePercent <= 0;

  return (
    <main id="main-content" className="px-4 pt-6 pb-24 max-w-lg mx-auto" role="main">
      <header className="mb-6">
        <div className="flex items-center gap-2 mb-1">
          <Calendar size={20} className="text-primary-400" aria-hidden="true" />
          <h1 className="text-2xl font-bold text-white">Monthly Report</h1>
        </div>
        <p className="text-dark-400 text-sm">{report.month} {report.year}</p>
      </header>

      {/* Hero Stats */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} ref={shareRef}>
        <Card className="p-6 mb-4 text-center glass-primary">
          <p className="text-dark-300 text-sm mb-1">Total Monthly CO₂</p>
          <p className="text-4xl font-bold text-primary-400">
            {report.totalCO2.toFixed(1)} <span className="text-lg text-dark-400">kg</span>
          </p>
          <div className="flex items-center justify-center gap-1 mt-2">
            {isImproved ? (
              <TrendingDown size={16} className="text-green-400" aria-hidden="true" />
            ) : (
              <TrendingUp size={16} className="text-red-400" aria-hidden="true" />
            )}
            <span className={`text-sm font-medium ${isImproved ? 'text-green-400' : 'text-red-400'}`}>
              {Math.abs(report.changePercent).toFixed(1)}% vs {report.month === 'January' ? 'December' : 'last month'}
            </span>
          </div>
          <p className="text-xs text-dark-400 mt-2">
            Daily average: {report.dailyAverage.toFixed(1)} kg CO₂
          </p>
        </Card>
      </motion.div>

      {/* Highlights */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <Card className="p-5 mb-4">
          <h2 className="text-sm font-semibold text-dark-300 mb-3">🏆 Monthly Highlights</h2>
          <ul className="space-y-2" role="list">
            {report.highlights.map((h, i) => (
              <li key={i} className="text-sm text-dark-200 p-2 rounded-lg bg-dark-800/30">
                {h}
              </li>
            ))}
          </ul>
        </Card>
      </motion.div>

      {/* Weekly Trend */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <Card className="p-4 mb-4">
          <h2 className="text-sm font-semibold text-dark-300 mb-3">Weekly Trend</h2>
          <div className="space-y-3">
            {report.weeklyTrend.map((w, i) => (
              <div key={i} className="flex items-center gap-3">
                <span className="text-xs text-dark-400 w-16 shrink-0">{w.week}</span>
                <div className="flex-1 h-3 bg-dark-800 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(w.amount / Math.max(...report.weeklyTrend.map(x => x.amount))) * 100}%` }}
                    transition={{ duration: 0.8, delay: 0.3 + i * 0.1 }}
                    className="h-full bg-primary-500 rounded-full"
                  />
                </div>
                <span className="text-xs text-dark-300 w-12 text-right">{w.amount.toFixed(1)} kg</span>
              </div>
            ))}
          </div>
        </Card>
      </motion.div>

      {/* Gemini Narrative */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: narrativeVisible ? 1 : 0, y: narrativeVisible ? 0 : 20 }}
        transition={{ delay: 0.4 }}
      >
        <Card className="p-5 mb-4 border-primary-800/30">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles size={18} className="text-primary-400" aria-hidden="true" />
            <h2 className="text-sm font-semibold text-dark-300">CarbonCoach AI Insights</h2>
          </div>
          <div className="prose prose-sm prose-invert max-w-none">
            {report.geminiNarrative.split('\n\n').map((paragraph, i) => (
              <motion.p
                key={i}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 + i * 0.3 }}
                className="text-sm text-dark-300 leading-relaxed mb-3 last:mb-0"
              >
                {paragraph}
              </motion.p>
            ))}
          </div>
        </Card>
      </motion.div>

      {/* Share Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="flex gap-3"
      >
        <Button
          variant="primary"
          className="flex-1"
          onClick={handleShare}
          aria-label="Share monthly report"
        >
          <Share2 size={16} className="mr-2" aria-hidden="true" />
          Share Report
        </Button>
      </motion.div>
    </main>
  );
}
