/**
 * @fileoverview Profile result screen shown after onboarding completion.
 * Displays carbon score, estimates, and personalized recommendations.
 */
import React, { useEffect, useState, useCallback, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Leaf,
  TrendingDown,
  Target,
  Lightbulb,
  ArrowRight,
} from 'lucide-react';
import type { CarbonProfile } from '@/types';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

interface ProfileResultProps {
  /** Carbon profile data */
  profile: CarbonProfile;
  /** Callback when user clicks continue */
  onContinue: () => void;
}

/**
 * Animated count-up hook for number displays.
 * @param target - Target number to count up to
 * @param duration - Animation duration in ms
 */
function useCountUp(target: number, duration: number = 1500): number {
  const [count, setCount] = useState(0);
  const startTimeRef = useRef<number | null>(null);
  const frameRef = useRef<number>(0);

  useEffect(() => {
    startTimeRef.current = null;

    const animate = (timestamp: number) => {
      if (!startTimeRef.current) startTimeRef.current = timestamp;
      const progress = Math.min((timestamp - startTimeRef.current) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // Ease-out cubic
      setCount(Math.round(target * eased * 10) / 10);

      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate);
      }
    };

    frameRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frameRef.current);
  }, [target, duration]);

  return count;
}

/**
 * Profile result screen with animated score reveal, carbon estimates,
 * and personalized recommendations after onboarding.
 * @param props - ProfileResult properties including profile data and continue callback
 */
const ProfileResult = React.memo<ProfileResultProps>(function ProfileResult({
  profile,
  onContinue,
}) {
  const animatedScore = useCountUp(profile.carbonScore, 2000);
  const animatedYearly = useCountUp(profile.yearlyEstimate, 2500);

  const getScoreColor = useCallback((score: number): string => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-primary-400';
    if (score >= 40) return 'text-amber-400';
    return 'text-red-400';
  }, []);

  const getScoreLabel = useCallback((score: number): string => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Average';
    return 'Needs Improvement';
  }, []);

  return (
    <div className="min-h-dvh gradient-dark overflow-y-auto">
      <div className="fixed inset-0 gradient-radial pointer-events-none" aria-hidden="true" />

      <div className="relative z-10 px-6 py-12 max-w-md mx-auto space-y-8">
        {/* Header */}
        <motion.div
          className="text-center space-y-2"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-3xl font-bold text-dark-100">Your Carbon Profile</h1>
          <p className="text-dark-400">Here's your personalized carbon footprint estimate</p>
        </motion.div>

        {/* Carbon Score Circle */}
        <motion.div
          className="flex justify-center"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.6, type: 'spring' }}
        >
          <div className="relative w-44 h-44">
            {/* Outer ring */}
            <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120" aria-hidden="true">
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke="rgba(30, 41, 59, 0.6)"
                strokeWidth="8"
              />
              <motion.circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke="#16a34a"
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 52}`}
                initial={{ strokeDashoffset: 2 * Math.PI * 52 }}
                animate={{
                  strokeDashoffset:
                    2 * Math.PI * 52 * (1 - profile.carbonScore / 100),
                }}
                transition={{ duration: 2, ease: 'easeOut', delay: 0.5 }}
              />
            </svg>
            {/* Center text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className={`text-4xl font-bold ${getScoreColor(profile.carbonScore)}`}>
                {Math.round(animatedScore)}
              </span>
              <span className="text-xs text-dark-400 mt-1">{getScoreLabel(profile.carbonScore)}</span>
            </div>
          </div>
        </motion.div>

        {/* Emission Estimates */}
        <motion.div
          className="grid grid-cols-3 gap-3"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.5 }}
        >
          {[
            { label: 'Weekly', value: profile.weeklyEstimate, unit: 'kg' },
            { label: 'Monthly', value: profile.monthlyEstimate, unit: 'kg' },
            { label: 'Yearly', value: profile.yearlyEstimate, unit: 'kg' },
          ].map((item) => (
            <Card key={item.label} variant="light" padding="sm" className="text-center">
              <p className="text-lg font-bold text-dark-100">
                {item.label === 'Yearly' ? animatedYearly.toFixed(0) : item.value.toFixed(0)}
              </p>
              <p className="text-xs text-dark-400">
                {item.unit} CO₂/{item.label.toLowerCase()}
              </p>
            </Card>
          ))}
        </motion.div>

        {/* Benchmark comparison */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.5 }}
        >
          <Card variant="primary" className="space-y-3">
            <div className="flex items-center gap-2">
              <Target className="w-5 h-5 text-primary-400" aria-hidden="true" />
              <h3 className="font-semibold text-dark-100">How You Compare</h3>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-dark-400">You</span>
              <span className="text-primary-400 font-semibold">
                {profile.yearlyEstimate.toFixed(0)} kg/year
              </span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-dark-400">National Average</span>
              <span className="text-dark-300 font-semibold">
                {profile.nationalAverage.toFixed(0)} kg/year
              </span>
            </div>
            <div className="flex items-center gap-2 pt-1">
              <TrendingDown className="w-4 h-4 text-green-400" aria-hidden="true" />
              <span className="text-sm text-green-400 font-medium">
                {profile.percentile}th percentile — better than {100 - profile.percentile}% of users!
              </span>
            </div>
          </Card>
        </motion.div>

        {/* Recommendations */}
        <motion.div
          className="space-y-3"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0, duration: 0.5 }}
        >
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-amber-400" aria-hidden="true" />
            <h3 className="font-semibold text-dark-100">Personalized Tips</h3>
          </div>
          {profile.recommendations.map((tip, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.2 + index * 0.15 }}
            >
              <Card variant="light" padding="sm" className="flex items-start gap-3">
                <Leaf className="w-4 h-4 text-primary-400 shrink-0 mt-0.5" aria-hidden="true" />
                <p className="text-sm text-dark-300">{tip}</p>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.6, duration: 0.5 }}
        >
          <Button
            fullWidth
            size="lg"
            onClick={onContinue}
            icon={<ArrowRight className="w-5 h-5" />}
            aria-label="Go to your dashboard"
          >
            Start Tracking
          </Button>
        </motion.div>
      </div>
    </div>
  );
});

export default ProfileResult;
