/**
 * @fileoverview Carbon emission constants for client-side CO2 previews.
 * All values are in kg CO2 equivalent.
 */

/** Transport emissions per kilometer (kg CO2e/km) */
export const TRANSPORT_EMISSIONS = {
  car_petrol: 0.21,
  car_ev: 0.05,
  bus: 0.089,
  train: 0.041,
  motorbike: 0.114,
  flight_short: 0.255,
  flight_long: 0.195,
} as const;

/** Food emissions per meal (kg CO2e/meal) */
export const FOOD_EMISSIONS = {
  beef_meal: 6.0,
  chicken_meal: 1.5,
  fish_meal: 1.2,
  vegetarian_meal: 0.7,
  vegan_meal: 0.4,
} as const;

/** Energy emissions per kWh (kg CO2e/kWh) */
export const ENERGY_EMISSIONS = {
  india_grid: 0.82,
  renewable: 0.02,
} as const;

/** Shopping emissions per ₹1000 spent (kg CO2e/₹1000) */
export const SHOPPING_EMISSIONS = {
  clothing: 0.4,
  electronics: 0.8,
  groceries: 0.2,
  other: 0.3,
} as const;

/** Type for transport sub-categories */
export type TransportType = keyof typeof TRANSPORT_EMISSIONS;

/** Type for food sub-categories */
export type FoodType = keyof typeof FOOD_EMISSIONS;

/** Type for energy sub-categories */
export type EnergyType = keyof typeof ENERGY_EMISSIONS;

/** Type for shopping sub-categories */
export type ShoppingType = keyof typeof SHOPPING_EMISSIONS;

/** Activity category types */
export type ActivityCategory = 'transport' | 'food' | 'energy' | 'shopping';

/** Human-readable labels for transport types */
export const TRANSPORT_LABELS: Record<TransportType, string> = {
  car_petrol: 'Car (Petrol)',
  car_ev: 'Electric Car',
  bus: 'Bus',
  train: 'Train',
  motorbike: 'Motorbike',
  flight_short: 'Flight (Short)',
  flight_long: 'Flight (Long)',
};

/** Human-readable labels for food types */
export const FOOD_LABELS: Record<FoodType, string> = {
  beef_meal: 'Beef Meal',
  chicken_meal: 'Chicken Meal',
  fish_meal: 'Fish Meal',
  vegetarian_meal: 'Vegetarian Meal',
  vegan_meal: 'Vegan Meal',
};

/** Human-readable labels for energy types */
export const ENERGY_LABELS: Record<EnergyType, string> = {
  india_grid: 'Grid Electricity',
  renewable: 'Renewable Energy',
};

/** Human-readable labels for shopping types */
export const SHOPPING_LABELS: Record<ShoppingType, string> = {
  clothing: 'Clothing',
  electronics: 'Electronics',
  groceries: 'Groceries',
  other: 'Other',
};

/**
 * Calculate CO2 emissions for a given activity.
 * @param category - The activity category
 * @param subType - The sub-type within the category
 * @param quantity - The quantity (km, meals, kWh, or ₹1000 units)
 * @returns CO2 emissions in kg
 */
export function calculateEmissions(
  category: ActivityCategory,
  subType: string,
  quantity: number,
): number {
  switch (category) {
    case 'transport':
      return (TRANSPORT_EMISSIONS[subType as TransportType] ?? 0) * quantity;
    case 'food':
      return (FOOD_EMISSIONS[subType as FoodType] ?? 0) * quantity;
    case 'energy':
      return (ENERGY_EMISSIONS[subType as EnergyType] ?? 0) * quantity;
    case 'shopping':
      return (SHOPPING_EMISSIONS[subType as ShoppingType] ?? 0) * quantity;
    default:
      return 0;
  }
}

/** Category color mapping for charts */
export const CATEGORY_COLORS: Record<ActivityCategory, string> = {
  transport: '#3b82f6',
  food: '#f59e0b',
  energy: '#a855f7',
  shopping: '#ec4899',
};

/** Category icon names for lucide-react */
export const CATEGORY_ICONS: Record<ActivityCategory, string> = {
  transport: 'Car',
  food: 'UtensilsCrossed',
  energy: 'Zap',
  shopping: 'ShoppingBag',
};
