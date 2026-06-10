/**
 * @fileoverview Challenges list screen.
 * Shows current active challenge and past challenges.
 */
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Trophy, Target, Clock, CheckCircle2, ChevronRight, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Card, Badge, Skeleton, ProgressBar } from '@/components/ui';
import { useToast } from '@/components/ui/Toast';
import { type ActivityCategory } from '@/lib/carbon-constants';
import { api } from '@/lib/api';
import type { Challenge } from '@/types';

/** Category icon map */
const CATEGORY_EMOJI: Record<ActivityCategory, string> = {
  transport: '🚗',
  food: '🍽',
  energy: '⚡',
  shopping: '🛍',
};

/** Mock challenges for demo */
const MOCK_CHALLENGES: Challenge[] = [
  {
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
    tips: ['Try the metro during non-peak hours for a comfortable ride.'],
  },
  {
    id: '2026-W22',
    title: 'Meatless Monday Champion',
    description: 'Go fully vegetarian on Monday. Try that new paneer place!',
    category: 'food',
    difficulty: 'easy',
    durationDays: 7,
    co2SavedTarget: 5.3,
    co2SavedActual: 5.3,
    progress: 100,
    status: 'completed',
    participants: 412,
    tips: [],
  },
  {
    id: '2026-W21',
    title: 'Lights Out Challenge',
    description: 'Reduce energy usage by 15% compared to last week.',
    category: 'energy',
    difficulty: 'hard',
    durationDays: 7,
    co2SavedTarget: 3.8,
    co2SavedActual: 1.2,
    progress: 32,
    status: 'expired',
    participants: 189,
    tips: [],
  },
];

/**
 * Challenges list screen.
 */
export default function ChallengesScreen() {
  const navigate = useNavigate();
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);
  const [suggestCategory, setSuggestCategory] = useState<ActivityCategory>('transport');
  const [suggesting, setSuggesting] = useState(false);
  const { addToast } = useToast();

  const handleRequestSuggestion = async () => {
    setSuggesting(true);
    try {
      const res = await api.post<Challenge>(`/challenge/suggest/${suggestCategory}`, {});
      setChallenges((prev) => {
        const filtered = prev.filter((c) => c.id !== res.data.id);
        return [res.data, ...filtered];
      });
      addToast({
        type: 'success',
        title: '🌿 AI Challenge Activated!',
        message: `Your custom challenge "${res.data.title}" is now active. Good luck!`,
        duration: 6000,
      });
    } catch {
      addToast({
        type: 'error',
        title: 'Suggestion Failed',
        message: 'Could not communicate with Gemini. Please try again.',
      });
    } finally {
      setSuggesting(false);
    }
  };

  useEffect(() => {
    async function fetchChallenges() {
      try {
        const res = await api.get<Challenge[]>('/challenge/list');
        setChallenges(res.data);
      } catch {
        setChallenges(MOCK_CHALLENGES);
      } finally {
        setLoading(false);
      }
    }
    fetchChallenges();
  }, []);

  const active = challenges.filter((c) => c.status === 'active');
  const past = challenges.filter((c) => c.status !== 'active');

  if (loading) {
    return (
      <div className="px-4 pt-6 pb-24 max-w-lg mx-auto space-y-4" role="status">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-40 w-full rounded-2xl" />
        <Skeleton className="h-24 w-full rounded-2xl" />
        <span className="sr-only">Loading challenges...</span>
      </div>
    );
  }

  return (
    <main id="main-content" className="px-4 pt-6 pb-24 max-w-lg mx-auto" role="main">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Trophy size={24} className="text-primary-400" aria-hidden="true" />
          Challenges
        </h1>
        <p className="text-dark-400 text-sm mt-1">
          Weekly AI-powered missions to reduce your footprint
        </p>
      </header>

      {/* Request Custom AI Challenge */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-4 mb-6 border-primary-500/20"
      >
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-white flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-primary-400" aria-hidden="true" />
            Get Custom AI Challenge
          </h2>
          <span className="text-[10px] bg-primary-600/20 text-primary-400 px-2 py-0.5 rounded-full font-medium">
            Gemini Powered
          </span>
        </div>
        <p className="text-xs text-dark-400 mb-3">
          Ask CarbonCoach to draft a custom emissions-reduction challenge for a specific category.
        </p>
        <div className="flex gap-2">
          <select
            value={suggestCategory}
            onChange={(e) => setSuggestCategory(e.target.value as ActivityCategory)}
            className="bg-dark-900 border border-dark-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-primary-500 cursor-pointer"
            aria-label="Select category for AI challenge suggestion"
            disabled={suggesting}
          >
            <option value="transport">🚗 Transport</option>
            <option value="food">🍽 Food</option>
            <option value="energy">⚡ Energy</option>
            <option value="shopping">🛍 Shopping</option>
          </select>
          <button
            onClick={handleRequestSuggestion}
            disabled={suggesting}
            className="flex-1 px-4 py-2 text-xs font-semibold rounded-xl bg-primary-600 hover:bg-primary-500 disabled:bg-dark-800 disabled:text-dark-500 text-white transition-colors cursor-pointer focus-visible:outline-2 focus-visible:outline-primary-500"
          >
            {suggesting ? 'Generating Challenge...' : 'Suggest Challenge'}
          </button>
        </div>
      </motion.div>

      {/* Active Challenges */}
      {active.length > 0 && (
        <section aria-label="Active challenges" className="mb-8">
          <h2 className="text-sm font-semibold text-dark-300 uppercase tracking-wide mb-3">
            This Week's Mission
          </h2>
          {active.map((challenge, i) => (
            <motion.div
              key={challenge.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
            >
              <button
                onClick={() => navigate(`/challenges/${challenge.id}`)}
                className="w-full text-left mb-3"
                aria-label={`View challenge: ${challenge.title}`}
                type="button"
              >
                <Card className="p-5 border-primary-700/30 hover:border-primary-600/50 transition-all">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl" role="img" aria-label={challenge.category}>
                        {CATEGORY_EMOJI[challenge.category]}
                      </span>
                      <div>
                        <h3 className="text-base font-semibold text-white">{challenge.title}</h3>
                        <Badge variant="primary" className="mt-1">
                          {challenge.difficulty}
                        </Badge>
                      </div>
                    </div>
                    <ChevronRight size={18} className="text-dark-400 mt-1" aria-hidden="true" />
                  </div>
                  <p className="text-sm text-dark-400 mb-4">{challenge.description}</p>
                  <ProgressBar
                    value={challenge.progress}
                    max={100}
                    ariaLabel="Challenge progress"
                  />
                  <div className="flex justify-between items-center mt-3 text-xs text-dark-400">
                    <span>
                      🌱 {challenge.co2SavedActual.toFixed(1)} /{' '}
                      {challenge.co2SavedTarget.toFixed(1)} kg CO₂ saved
                    </span>
                    <span>{challenge.participants} participants</span>
                  </div>
                </Card>
              </button>
            </motion.div>
          ))}
        </section>
      )}

      {/* Past Challenges */}
      {past.length > 0 && (
        <section aria-label="Past challenges">
          <h2 className="text-sm font-semibold text-dark-300 uppercase tracking-wide mb-3">
            Past Challenges
          </h2>
          {past.map((challenge, i) => (
            <motion.div
              key={challenge.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + i * 0.1 }}
            >
              <Card className="p-4 mb-3 opacity-80">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-xl" role="img" aria-label={challenge.category}>
                      {CATEGORY_EMOJI[challenge.category]}
                    </span>
                    <div>
                      <h3 className="text-sm font-medium text-white">{challenge.title}</h3>
                      <div className="flex items-center gap-2 mt-1">
                        {challenge.status === 'completed' ? (
                          <Badge variant="success" className="text-xs">
                            <CheckCircle2 size={12} className="mr-1" aria-hidden="true" /> Completed
                          </Badge>
                        ) : (
                          <Badge variant="default" className="text-xs">
                            <Clock size={12} className="mr-1" aria-hidden="true" /> Expired
                          </Badge>
                        )}
                        <span className="text-xs text-dark-500">
                          {challenge.co2SavedActual.toFixed(1)} kg saved
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </section>
      )}

      {/* Empty state */}
      {challenges.length === 0 && (
        <div className="text-center py-12">
          <Target size={48} className="text-dark-600 mx-auto mb-3" aria-hidden="true" />
          <p className="text-dark-400">No challenges yet. Your first mission drops Monday!</p>
        </div>
      )}
    </main>
  );
}
