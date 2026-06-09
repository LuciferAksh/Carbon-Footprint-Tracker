/**
 * @fileoverview Challenge detail screen with progress tracker and completion button.
 */
import { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, CheckCircle2, Target, Leaf, Users } from 'lucide-react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Badge, ProgressBar, Skeleton } from '@/components/ui';
import { api } from '@/lib/api';
import type { Challenge } from '@/types';

/** Mock challenge detail */
const MOCK_CHALLENGE: Challenge = {
  id: '2026-W23', title: 'Metro Week Challenge',
  description: 'Take public transport at least 3 times this week instead of your car. The metro is fast, reliable, and saves ~4.2 kg CO₂ compared to driving.',
  category: 'transport', difficulty: 'medium', durationDays: 7,
  co2SavedTarget: 4.2, co2SavedActual: 1.8, progress: 43,
  status: 'active', participants: 234,
  tips: [
    'Try the metro during non-peak hours for a comfortable ride',
    'Use Google Maps for public transport routes — often faster than driving!',
    'Track each trip in the Log tab to see your savings grow',
  ],
};

/**
 * Challenge detail screen.
 */
export default function ChallengeDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [challenge, setChallenge] = useState<Challenge | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);

  useEffect(() => {
    async function fetchChallenge() {
      try {
        const res = await api.get<Challenge>(`/challenge/${id}`);
        setChallenge(res.data);
      } catch {
        setChallenge(MOCK_CHALLENGE);
      } finally {
        setLoading(false);
      }
    }
    fetchChallenge();
  }, [id]);

  const handleComplete = useCallback(async () => {
    if (!challenge) return;
    setCompleting(true);
    try {
      await api.patch(`/challenge/${challenge.id}/complete`, {});
      setChallenge({ ...challenge, status: 'completed', progress: 100 });
    } catch {
      setChallenge({ ...challenge, status: 'completed', progress: 100 });
    } finally {
      setCompleting(false);
    }
  }, [challenge]);

  if (loading) {
    return (
      <div className="px-4 pt-6 pb-24 max-w-lg mx-auto space-y-4" role="status">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-60 w-full rounded-2xl" />
        <span className="sr-only">Loading challenge...</span>
      </div>
    );
  }

  if (!challenge) return null;

  const isCompleted = challenge.status === 'completed';

  return (
    <main id="main-content" className="px-4 pt-6 pb-24 max-w-lg mx-auto" role="main">
      {/* Back button */}
      <button
        onClick={() => navigate('/challenges')}
        className="flex items-center gap-1 text-dark-400 hover:text-white transition-colors mb-4"
        aria-label="Back to challenges"
        type="button"
      >
        <ArrowLeft size={18} aria-hidden="true" />
        <span className="text-sm">Back</span>
      </button>

      {/* Challenge Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <Card className="p-6 mb-4">
          <div className="flex items-center gap-2 mb-3">
            <Badge variant={isCompleted ? 'success' : 'primary'}>
              {isCompleted ? '✅ Completed' : '🔥 Active'}
            </Badge>
            <Badge variant="default">{challenge.difficulty}</Badge>
          </div>

          <h1 className="text-xl font-bold text-white mb-2">{challenge.title}</h1>
          <p className="text-dark-400 text-sm mb-4">{challenge.description}</p>

          {/* Progress */}
          <div className="mb-4">
            <div className="flex justify-between text-xs text-dark-400 mb-2">
              <span>Progress</span>
              <span>{challenge.progress}%</span>
            </div>
            <ProgressBar
              value={challenge.progress}
              max={100}
              ariaLabel="Challenge completion progress"
            />
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="p-3 rounded-xl bg-dark-800/50">
              <Target size={16} className="text-primary-400 mx-auto mb-1" aria-hidden="true" />
              <p className="text-sm font-bold text-white">{challenge.co2SavedTarget.toFixed(1)}</p>
              <p className="text-xs text-dark-400">kg target</p>
            </div>
            <div className="p-3 rounded-xl bg-dark-800/50">
              <Leaf size={16} className="text-green-400 mx-auto mb-1" aria-hidden="true" />
              <p className="text-sm font-bold text-white">{challenge.co2SavedActual.toFixed(1)}</p>
              <p className="text-xs text-dark-400">kg saved</p>
            </div>
            <div className="p-3 rounded-xl bg-dark-800/50">
              <Users size={16} className="text-blue-400 mx-auto mb-1" aria-hidden="true" />
              <p className="text-sm font-bold text-white">{challenge.participants}</p>
              <p className="text-xs text-dark-400">joined</p>
            </div>
          </div>
        </Card>
      </motion.div>

      {/* Tips */}
      {challenge.tips.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <Card className="p-5 mb-4">
            <h2 className="text-sm font-semibold text-dark-300 mb-3">💡 Tips from CarbonCoach</h2>
            <ul className="space-y-2" role="list">
              {challenge.tips.map((tip, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-dark-300">
                  <span className="text-primary-400 mt-0.5 shrink-0">•</span>
                  {tip}
                </li>
              ))}
            </ul>
          </Card>
        </motion.div>
      )}

      {/* Complete Button */}
      {!isCompleted && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Button
            variant="primary"
            className="w-full"
            onClick={handleComplete}
            disabled={completing}
            aria-label="Mark challenge as completed"
          >
            {completing ? (
              'Completing...'
            ) : (
              <span className="flex items-center gap-2">
                <CheckCircle2 size={18} aria-hidden="true" />
                Mark as Completed
              </span>
            )}
          </Button>
        </motion.div>
      )}

      {/* Completed celebration */}
      {isCompleted && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center py-6"
        >
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 0.5 }}
            className="text-5xl mb-3"
          >
            🎉
          </motion.div>
          <p className="text-lg font-semibold text-primary-400">Challenge Completed!</p>
          <p className="text-sm text-dark-400 mt-1">
            You saved {challenge.co2SavedActual.toFixed(1)} kg CO₂ this week
          </p>
        </motion.div>
      )}
    </main>
  );
}
