import { describe, it, expect } from 'vitest';
import { calculateEmissions } from '../lib/carbon-constants';

describe('calculateEmissions', () => {
  it('should calculate transport emissions correctly', () => {
    expect(calculateEmissions('transport', 'car_petrol', 10)).toBeCloseTo(2.1);
    expect(calculateEmissions('transport', 'car_ev', 100)).toBeCloseTo(5.0);
    expect(calculateEmissions('transport', 'bus', 50)).toBeCloseTo(4.45);
  });

  it('should calculate food emissions correctly', () => {
    expect(calculateEmissions('food', 'beef_meal', 2)).toBeCloseTo(12.0);
    expect(calculateEmissions('food', 'vegan_meal', 5)).toBeCloseTo(2.0);
  });

  it('should calculate energy emissions correctly', () => {
    expect(calculateEmissions('energy', 'india_grid', 10)).toBeCloseTo(8.2);
    expect(calculateEmissions('energy', 'renewable', 100)).toBeCloseTo(2.0);
  });

  it('should calculate shopping emissions correctly', () => {
    expect(calculateEmissions('shopping', 'electronics', 2.5)).toBeCloseTo(2.0);
  });

  it('should return 0 for unknown category or type', () => {
    expect(calculateEmissions('invalid' as any, 'any', 10)).toBe(0);
    expect(calculateEmissions('transport', 'unknown_type', 10)).toBe(0);
  });

  it('should handle zero or negative quantities', () => {
    expect(calculateEmissions('transport', 'car_petrol', 0)).toBe(0);
    expect(calculateEmissions('transport', 'car_petrol', -10)).toBeCloseTo(-2.1);
  });
});
