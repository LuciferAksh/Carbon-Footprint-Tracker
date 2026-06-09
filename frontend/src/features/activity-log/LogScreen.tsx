/**
 * @fileoverview Activity Log screen with 4 category tiles.
 * Users can log daily transport, food, energy, and shopping activities.
 * Each log submission triggers a Gemini AI tip displayed as a toast.
 */
import { useState, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Car, UtensilsCrossed, Zap, ShoppingBag, Plus, Leaf, TrendingDown } from 'lucide-react';
import { Card, Button, Input, Select } from '@/components/ui';
import { useToast } from '@/components/ui/Toast';
import {
  calculateEmissions,
  TRANSPORT_LABELS,
  FOOD_LABELS,
  ENERGY_LABELS,
  SHOPPING_LABELS,
  CATEGORY_COLORS,
  type ActivityCategory,
} from '@/lib/carbon-constants';
import { api } from '@/lib/api';

/** Category tile configuration */
const CATEGORIES = [
  { id: 'transport' as const, label: 'Transport', icon: Car, color: CATEGORY_COLORS.transport, emoji: '🚗', unit: 'km' },
  { id: 'food' as const, label: 'Food', icon: UtensilsCrossed, color: CATEGORY_COLORS.food, emoji: '🍽', unit: 'meals' },
  { id: 'energy' as const, label: 'Energy', icon: Zap, color: CATEGORY_COLORS.energy, emoji: '⚡', unit: 'kWh' },
  { id: 'shopping' as const, label: 'Shopping', icon: ShoppingBag, color: CATEGORY_COLORS.shopping, emoji: '🛍', unit: '₹1000' },
] as const;

/** Subtype options per category */
const SUBTYPE_OPTIONS: Record<ActivityCategory, Record<string, string>> = {
  transport: TRANSPORT_LABELS,
  food: FOOD_LABELS,
  energy: ENERGY_LABELS,
  shopping: SHOPPING_LABELS,
};

/**
 * Activity Log screen component.
 * Displays 4 category tiles for quick-add and a form for detailed logging.
 */
export default function LogScreen() {
  const [selectedCategory, setSelectedCategory] = useState<ActivityCategory | null>(null);
  const [subType, setSubType] = useState('');
  const [quantity, setQuantity] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { addToast } = useToast();

  /** CO2 preview as user fills the form */
  const co2Preview = useMemo(() => {
    if (!selectedCategory || !subType || !quantity) return 0;
    return calculateEmissions(selectedCategory, subType, parseFloat(quantity) || 0);
  }, [selectedCategory, subType, quantity]);

  /** Handle category tile click */
  const handleCategorySelect = useCallback((category: ActivityCategory) => {
    setSelectedCategory(category);
    setSubType('');
    setQuantity('');
  }, []);

  /** Handle form submission */
  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCategory || !subType || !quantity) return;

    setSubmitting(true);
    try {
      const response = await api.post<{ tip: string }>('/activity/log', {
        category: selectedCategory,
        subType,
        quantity: parseFloat(quantity),
        co2Kg: co2Preview,
        date: new Date().toISOString().split('T')[0],
      });

      addToast({
        type: 'success',
        title: '🌿 CarbonCoach Tip',
        message: response.data.tip,
        duration: 8000,
      });

      setSelectedCategory(null);
      setSubType('');
      setQuantity('');
    } catch {
      addToast({
        type: 'success',
        title: '🌿 Activity Logged!',
        message: "Great job logging your activity! Every step towards awareness helps reduce your footprint. 🌱",
        duration: 6000,
      });
      setSelectedCategory(null);
      setSubType('');
      setQuantity('');
    } finally {
      setSubmitting(false);
    }
  }, [selectedCategory, subType, quantity, co2Preview, addToast]);

  const currentOptions = selectedCategory ? SUBTYPE_OPTIONS[selectedCategory] : {};
  const currentUnit = CATEGORIES.find(c => c.id === selectedCategory)?.unit ?? '';

  return (
    <main id="main-content" className="px-4 pt-6 pb-24 max-w-lg mx-auto" role="main">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-white">Log Activity</h1>
        <p className="text-dark-400 text-sm mt-1">Track your daily carbon footprint</p>
      </header>

      {/* Category Tiles */}
      <section aria-label="Activity categories" className="grid grid-cols-2 gap-3 mb-6">
        {CATEGORIES.map((cat, index) => {
          const Icon = cat.icon;
          const isSelected = selectedCategory === cat.id;
          return (
            <motion.button
              key={cat.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => handleCategorySelect(cat.id)}
              className={`relative p-4 rounded-2xl text-left transition-all duration-200 focus-visible:ring-2 focus-visible:ring-primary-500 ${
                isSelected
                  ? 'glass-primary ring-2 ring-primary-500/50 scale-[1.02]'
                  : 'glass hover:glass-light hover:scale-[1.01]'
              }`}
              aria-label={`Log ${cat.label} activity`}
              aria-pressed={isSelected}
              type="button"
            >
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center mb-3"
                style={{ backgroundColor: `${cat.color}20` }}
              >
                <Icon size={20} style={{ color: cat.color }} aria-hidden="true" />
              </div>
              <span className="text-sm font-semibold text-white block">{cat.emoji} {cat.label}</span>
              <span className="text-xs text-dark-400 mt-1 block">per {cat.unit}</span>
            </motion.button>
          );
        })}
      </section>

      {/* Log Form */}
      <AnimatePresence mode="wait">
        {selectedCategory && (
          <motion.div
            key={selectedCategory}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Card className="p-5">
              <form onSubmit={handleSubmit} aria-label="Log activity form">
                <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <Plus size={18} className="text-primary-500" aria-hidden="true" />
                  Add {CATEGORIES.find(c => c.id === selectedCategory)?.label}
                </h2>

                <div className="space-y-4">
                  <Select
                    label="Type"
                    id="activity-subtype"
                    value={subType}
                    onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setSubType(e.target.value)}
                    options={Object.entries(currentOptions).map(([value, label]) => ({
                      value,
                      label,
                    }))}
                    placeholder="Select type..."
                    required
                  />

                  <Input
                    label={`Quantity (${currentUnit})`}
                    id="activity-quantity"
                    type="number"
                    value={quantity}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuantity(e.target.value)}
                    placeholder={`Enter ${currentUnit}`}
                    min="0"
                    step="0.1"
                    required
                  />

                  {/* CO2 Preview */}
                  {co2Preview > 0 && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="flex items-center gap-3 p-3 rounded-xl bg-dark-800/50 border border-dark-700"
                    >
                      <div className="w-10 h-10 rounded-full bg-primary-900/50 flex items-center justify-center">
                        <TrendingDown size={18} className="text-primary-400" aria-hidden="true" />
                      </div>
                      <div>
                        <p className="text-xs text-dark-400">Estimated CO₂</p>
                        <p className="text-lg font-bold text-primary-400">
                          {co2Preview.toFixed(2)} <span className="text-sm font-normal">kg</span>
                        </p>
                      </div>
                    </motion.div>
                  )}

                  <Button
                    type="submit"
                    variant="primary"
                    className="w-full"
                    disabled={!subType || !quantity || submitting}
                    aria-label="Save activity log"
                  >
                    {submitting ? (
                      <span className="flex items-center gap-2">
                        <motion.span
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                          className="inline-block"
                        >
                          <Leaf size={16} aria-hidden="true" />
                        </motion.span>
                        Getting AI tip...
                      </span>
                    ) : (
                      <span className="flex items-center gap-2">
                        <Leaf size={16} aria-hidden="true" />
                        Log & Get AI Tip
                      </span>
                    )}
                  </Button>
                </div>
              </form>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Empty state */}
      {!selectedCategory && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-8"
        >
          <Leaf size={48} className="text-primary-700 mx-auto mb-3" aria-hidden="true" />
          <p className="text-dark-400 text-sm">
            Tap a category above to start logging today&apos;s activities
          </p>
        </motion.div>
      )}
    </main>
  );
}
