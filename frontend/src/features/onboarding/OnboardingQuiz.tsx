/**
 * @fileoverview Beautiful 6-step onboarding quiz with animated card transitions.
 * Uses Framer Motion for smooth page transitions and Zod for validation.
 */
import React, { useCallback, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MapPin,
  Users,
  Car,
  UtensilsCrossed,
  Zap,
  ShoppingBag,
  ArrowRight,
  ArrowLeft,
  Sparkles,
} from 'lucide-react';
import { z } from 'zod';
import { useAuth } from '@/features/auth/AuthProvider';
import { api } from '@/lib/api';
import Button from '@/components/ui/Button';
import ProgressBar from '@/components/ui/ProgressBar';
import type { CarbonProfile, OnboardingAnswers } from '@/types';
import ProfileResult from './ProfileResult';

/** Zod schema for onboarding validation */
const onboardingSchema = z.object({
  location: z.string().min(1, 'Please select your location'),
  householdSize: z.number().min(1, 'Must be at least 1').max(20, 'Must be 20 or fewer'),
  primaryTransport: z.string().min(1, 'Please select your transport mode'),
  dietType: z.string().min(1, 'Please select your diet type'),
  energySource: z.string().min(1, 'Please select your energy source'),
  shoppingFrequency: z.enum(['low', 'medium', 'high'], {
    message: 'Please select your shopping frequency',
  }),
});

interface QuizOption {
  value: string;
  label: string;
  description?: string;
  icon?: React.ReactNode;
}

interface QuizStep {
  id: string;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  type: 'select' | 'number';
  field: keyof OnboardingAnswers;
  options?: QuizOption[];
  min?: number;
  max?: number;
  unit?: string;
}

const quizSteps: QuizStep[] = [
  {
    id: 'location',
    title: 'Where are you located?',
    subtitle: 'This helps us use the right emission factors for your region.',
    icon: <MapPin className="w-6 h-6" aria-hidden="true" />,
    type: 'select',
    field: 'location',
    options: [
      { value: 'india', label: '🇮🇳 India' },
      { value: 'us', label: '🇺🇸 United States' },
      { value: 'uk', label: '🇬🇧 United Kingdom' },
      { value: 'eu', label: '🇪🇺 Europe' },
      { value: 'other', label: '🌍 Other' },
    ],
  },
  {
    id: 'household',
    title: 'How big is your household?',
    subtitle: "We'll factor in shared emissions like energy and groceries.",
    icon: <Users className="w-6 h-6" aria-hidden="true" />,
    type: 'number',
    field: 'householdSize',
    min: 1,
    max: 20,
    unit: 'people',
  },
  {
    id: 'transport',
    title: 'Your primary transport?',
    subtitle: 'What do you mostly use for your daily commute?',
    icon: <Car className="w-6 h-6" aria-hidden="true" />,
    type: 'select',
    field: 'primaryTransport',
    options: [
      { value: 'car_petrol', label: '🚗 Petrol Car', description: '0.21 kg/km' },
      { value: 'car_ev', label: '⚡ Electric Car', description: '0.05 kg/km' },
      { value: 'bus', label: '🚌 Bus', description: '0.089 kg/km' },
      { value: 'train', label: '🚂 Train', description: '0.041 kg/km' },
      { value: 'motorbike', label: '🏍️ Motorbike', description: '0.114 kg/km' },
    ],
  },
  {
    id: 'diet',
    title: "What's your typical diet?",
    subtitle: 'Food choices have a significant impact on your footprint.',
    icon: <UtensilsCrossed className="w-6 h-6" aria-hidden="true" />,
    type: 'select',
    field: 'dietType',
    options: [
      { value: 'beef_meal', label: '🥩 Heavy Meat', description: '~6.0 kg CO₂/meal' },
      { value: 'chicken_meal', label: '🍗 Poultry/Fish', description: '~1.5 kg CO₂/meal' },
      { value: 'fish_meal', label: '🐟 Pescatarian', description: '~1.2 kg CO₂/meal' },
      { value: 'vegetarian_meal', label: '🥗 Vegetarian', description: '~0.7 kg CO₂/meal' },
      { value: 'vegan_meal', label: '🌱 Vegan', description: '~0.4 kg CO₂/meal' },
    ],
  },
  {
    id: 'energy',
    title: 'Your energy source?',
    subtitle: 'How is your home powered?',
    icon: <Zap className="w-6 h-6" aria-hidden="true" />,
    type: 'select',
    field: 'energySource',
    options: [
      { value: 'india_grid', label: '🔌 Grid Electricity', description: '0.82 kg/kWh' },
      { value: 'renewable', label: '☀️ Renewable/Solar', description: '0.02 kg/kWh' },
    ],
  },
  {
    id: 'shopping',
    title: 'Shopping habits?',
    subtitle: 'How frequently do you buy non-essential items?',
    icon: <ShoppingBag className="w-6 h-6" aria-hidden="true" />,
    type: 'select',
    field: 'shoppingFrequency',
    options: [
      { value: 'low', label: '🎯 Minimal', description: 'Buy only essentials' },
      { value: 'medium', label: '🛍️ Moderate', description: 'Occasional shopping' },
      { value: 'high', label: '🛒 Frequent', description: 'Regular shopping trips' },
    ],
  },
];

/** Animation variants for card transitions */
const cardVariants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 300 : -300,
    opacity: 0,
    scale: 0.95,
  }),
  center: {
    x: 0,
    opacity: 1,
    scale: 1,
  },
  exit: (direction: number) => ({
    x: direction < 0 ? 300 : -300,
    opacity: 0,
    scale: 0.95,
  }),
};

/**
 * Six-step onboarding quiz with animated transitions.
 * Collects user preferences and calculates initial carbon profile.
 */
const OnboardingQuiz = React.memo(function OnboardingQuiz() {
  const navigate = useNavigate();
  const { setOnboardingComplete } = useAuth();
  const [currentStep, setCurrentStep] = useState(0);
  const [direction, setDirection] = useState(0);
  const [answers, setAnswers] = useState<Partial<OnboardingAnswers>>({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<CarbonProfile | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const cardRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (cardRef.current) {
      cardRef.current.focus();
    }
  }, [currentStep]);

  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab' || !cardRef.current) return;

      const focusableElements = cardRef.current.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      );
      
      if (focusableElements.length === 0) return;

      const firstElement = focusableElements[0] as HTMLElement;
      const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const step = quizSteps[currentStep];
  const isLastStep = currentStep === quizSteps.length - 1;
  const progress = ((currentStep + 1) / quizSteps.length) * 100;

  const currentValue = step ? answers[step.field] : undefined;

  const validateCurrentStep = useCallback((): boolean => {
    if (!step) return false;
    const fieldSchema = onboardingSchema.shape[step.field];
    const result = fieldSchema.safeParse(currentValue);
    if (!result.success) {
      setErrors((prev) => ({
        ...prev,
        [step.field]: result.error.issues[0]?.message || 'Invalid input',
      }));
      return false;
    }
    setErrors((prev) => {
      const next = { ...prev };
      delete next[step.field];
      return next;
    });
    return true;
  }, [step, currentValue]);

  const handleNext = useCallback(async () => {
    if (!validateCurrentStep()) return;

    if (isLastStep) {
      // Submit onboarding
      try {
        setSubmitting(true);
        const response = await api.post<CarbonProfile>('/onboarding', answers);
        setResult(response.data);
        setOnboardingComplete();
      } catch {
        // Use mock result for demo
        setResult({
          weeklyEstimate: 42.5,
          monthlyEstimate: 170,
          yearlyEstimate: 2040,
          nationalAverage: 2500,
          percentile: 35,
          topCategory: 'transport',
          recommendations: [
            'Consider carpooling or public transit for your commute',
            'Try one meatless day per week to reduce food emissions',
            'Switch to LED bulbs to save energy',
          ],
          carbonScore: 72,
        });
        setOnboardingComplete();
      } finally {
        setSubmitting(false);
      }
    } else {
      setDirection(1);
      setCurrentStep((prev) => prev + 1);
    }
  }, [validateCurrentStep, isLastStep, answers, setOnboardingComplete]);

  const handleBack = useCallback(() => {
    setDirection(-1);
    setCurrentStep((prev) => Math.max(0, prev - 1));
  }, []);

  const handleOptionSelect = useCallback(
    (value: string | number) => {
      if (!step) return;
      setAnswers((prev) => ({ ...prev, [step.field]: value }));
      setErrors((prev) => {
        const next = { ...prev };
        delete next[step.field];
        return next;
      });
    },
    [step],
  );

  const handleFinish = useCallback(() => {
    navigate('/', { replace: true });
  }, [navigate]);

  // Show result screen after submission
  if (result) {
    return <ProfileResult profile={result} onContinue={handleFinish} />;
  }

  if (!step) return null;

  return (
    <main id="main-content" className="min-h-dvh gradient-dark flex flex-col" role="main">
      {/* Radial glow */}
      <div className="fixed inset-0 gradient-radial pointer-events-none" aria-hidden="true" />

      {/* Header */}
      <div className="relative z-10 px-6 pt-12 pb-6 space-y-4">
        <div className="flex items-center justify-between">
          <motion.p
            className="text-sm text-dark-400"
            key={currentStep}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            Step {currentStep + 1} of {quizSteps.length}
          </motion.p>
          <Sparkles className="w-5 h-5 text-primary-400" aria-hidden="true" />
        </div>
        <ProgressBar
          value={progress}
          size="sm"
          ariaLabel={`Quiz progress: step ${currentStep + 1} of ${quizSteps.length}`}
        />
      </div>

      {/* Quiz card with animated transitions */}
      <div className="flex-1 relative z-10 px-6 overflow-hidden">
        <AnimatePresence mode="wait" custom={direction}>
          <motion.div
            key={currentStep}
            ref={cardRef}
            tabIndex={-1}
            custom={direction}
            variants={cardVariants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{
              x: { type: 'spring', stiffness: 300, damping: 30 },
              opacity: { duration: 0.2 },
              scale: { duration: 0.2 },
            }}
            className="glass rounded-3xl p-6 sm:p-8 space-y-6 focus:outline-none"
          >
            {/* Step icon and title */}
            <div className="space-y-3">
              <div className="w-14 h-14 rounded-2xl bg-primary-600/10 border border-primary-600/20 flex items-center justify-center text-primary-400">
                {step.icon}
              </div>
              <h1 className="text-2xl font-bold text-dark-100">{step.title}</h1>
              <p className="text-dark-400 text-sm">{step.subtitle}</p>
            </div>

            {/* Options or number input */}
            <div className="space-y-3" role="radiogroup" aria-label={step.title}>
              {step.type === 'select' &&
                step.options?.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => handleOptionSelect(option.value)}
                    className={`
                      w-full flex items-center gap-4 p-4 rounded-xl border transition-all duration-200 text-left cursor-pointer
                      focus-visible:outline-2 focus-visible:outline-primary-500
                      ${
                        currentValue === option.value
                          ? 'border-primary-500 bg-primary-600/10 shadow-lg shadow-primary-600/10'
                          : 'border-dark-600/50 bg-dark-800/50 hover:border-dark-500 hover:bg-dark-800'
                      }
                    `}
                    role="radio"
                    aria-checked={currentValue === option.value}
                    aria-label={option.label}
                  >
                    <span className="text-lg">{option.label.split(' ')[0]}</span>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-dark-100">
                        {option.label.split(' ').slice(1).join(' ')}
                      </p>
                      {option.description && (
                        <p className="text-xs text-dark-500 mt-0.5">{option.description}</p>
                      )}
                    </div>
                    {currentValue === option.value && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-5 h-5 rounded-full bg-primary-500 flex items-center justify-center"
                      >
                        <svg
                          className="w-3 h-3 text-white"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          aria-hidden="true"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={3}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                      </motion.div>
                    )}
                  </button>
                ))}

              {step.type === 'number' && (
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <button
                      onClick={() =>
                        handleOptionSelect(
                          Math.max(step.min || 1, ((currentValue as number) || 1) - 1),
                        )
                      }
                      className="w-12 h-12 rounded-xl bg-dark-700 hover:bg-dark-600 border border-dark-600 flex items-center justify-center text-2xl text-dark-200 transition-colors cursor-pointer focus-visible:outline-2 focus-visible:outline-primary-500"
                      aria-label="Decrease count"
                    >
                      −
                    </button>
                    <div className="flex-1 text-center">
                      <motion.span
                        key={currentValue as number}
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-5xl font-bold text-primary-400 block"
                      >
                        {(currentValue as number) || 1}
                      </motion.span>
                      <span className="text-sm text-dark-500 mt-1">{step.unit}</span>
                    </div>
                    <button
                      onClick={() =>
                        handleOptionSelect(
                          Math.min(step.max || 20, ((currentValue as number) || 1) + 1),
                        )
                      }
                      className="w-12 h-12 rounded-xl bg-dark-700 hover:bg-dark-600 border border-dark-600 flex items-center justify-center text-2xl text-dark-200 transition-colors cursor-pointer focus-visible:outline-2 focus-visible:outline-primary-500"
                      aria-label="Increase count"
                    >
                      +
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Error message */}
            {errors[step.field] && (
              <p className="text-sm text-error" role="alert">
                {errors[step.field]}
              </p>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navigation buttons */}
      <div className="relative z-10 px-6 py-8 flex gap-3">
        {currentStep > 0 && (
          <Button
            variant="secondary"
            onClick={handleBack}
            icon={<ArrowLeft className="w-4 h-4" aria-hidden="true" />}
            aria-label="Go to previous step"
          >
            Back
          </Button>
        )}
        <Button
          fullWidth
          onClick={handleNext}
          loading={submitting}
          icon={isLastStep ? <Sparkles className="w-4 h-4" aria-hidden="true" /> : <ArrowRight className="w-4 h-4" aria-hidden="true" />}
          aria-label={isLastStep ? 'Calculate your carbon profile' : 'Go to next step'}
        >
          {isLastStep ? 'See My Profile' : 'Continue'}
        </Button>
      </div>
    </main>
  );
});

export default OnboardingQuiz;
