/**
 * @fileoverview Core TypeScript interfaces for the CarbonCoach application.
 */

import type {
  ActivityCategory,
  TransportType,
  FoodType,
  EnergyType,
  ShoppingType,
} from '@/lib/carbon-constants';

/** Firebase user profile */
export interface UserProfile {
  uid: string;
  email: string;
  displayName: string;
  photoURL: string | null;
  onboardingComplete: boolean;
  createdAt: string;
  carbonProfileType?: string;
  estimatedAnnualKg?: number;
  topCategories?: string[];
  carbonProfile?: CarbonProfile;
  streak?: number;
  badges?: string[];
}

/** Onboarding quiz answers */
export interface OnboardingAnswers {
  location: string;
  householdSize: number;
  primaryTransport: TransportType;
  dietType: FoodType;
  energySource: EnergyType;
  shoppingFrequency: 'low' | 'medium' | 'high';
}

/** Carbon profile result after onboarding */
export interface CarbonProfile {
  weeklyEstimate: number;
  monthlyEstimate: number;
  yearlyEstimate: number;
  nationalAverage: number;
  percentile: number;
  topCategory: ActivityCategory;
  recommendations: string[];
  carbonScore: number;
}

/** Activity log entry */
export interface ActivityEntry {
  id: string;
  userId: string;
  category: ActivityCategory;
  subType: TransportType | FoodType | EnergyType | ShoppingType;
  quantity: number;
  unit: string;
  co2Amount: number;
  date: string;
  notes?: string;
  aiTip?: string;
  createdAt: string;
}

/** Activity log form data */
export interface ActivityFormData {
  category: ActivityCategory;
  subType: string;
  quantity: number;
  date: string;
  notes?: string;
}

/** Dashboard weekly data point */
export interface WeeklyDataPoint {
  day: string;
  thisWeek: number;
  lastWeek: number;
}

/** Dashboard category breakdown */
export interface CategoryBreakdown {
  category: ActivityCategory;
  amount: number;
  percentage: number;
  color: string;
}

/** Dashboard summary */
export interface DashboardData {
  totalCO2Today: number;
  totalCO2Week: number;
  totalCO2Month: number;
  weeklyComparison: WeeklyDataPoint[];
  categoryBreakdown: CategoryBreakdown[];
  streak: number;
  carbonScore: number;
  benchmark: {
    user: number;
    national: number;
    target: number;
  };
}

/** Challenge */
export interface Challenge {
  id: string;
  title: string;
  description: string;
  category: ActivityCategory;
  difficulty: 'easy' | 'medium' | 'hard';
  durationDays: number;
  co2SavedTarget: number;
  co2SavedActual: number;
  progress: number;
  status: 'available' | 'active' | 'completed' | 'expired';
  startDate?: string;
  endDate?: string;
  participants: number;
  tips: string[];
}

/** Monthly report */
export interface MonthlyReport {
  month: string;
  year: number;
  totalCO2: number;
  previousMonthCO2: number;
  changePercent: number;
  dailyAverage: number;
  categoryBreakdown: CategoryBreakdown[];
  weeklyTrend: { week: string; amount: number }[];
  geminiNarrative: string;
  highlights: string[];
  score: number;
}

/** Navigation tab item */
export interface NavTab {
  path: string;
  label: string;
  icon: string;
}

/** Toast notification */
export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  title: string;
  message: string;
  duration?: number;
}
