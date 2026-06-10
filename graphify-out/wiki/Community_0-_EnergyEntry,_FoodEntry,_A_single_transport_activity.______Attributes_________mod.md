# Community 0: EnergyEntry, FoodEntry, A single transport activity.      Attributes         mod

> 75 nodes · cohesion 0.10

## Key Concepts

- **TransportEntry** (49 connections) — `backend\app\models\activity.py`
- **FoodEntry** (45 connections) — `backend\app\models\activity.py`
- **ShoppingEntry** (43 connections) — `backend\app\models\activity.py`
- **EnergyEntry** (42 connections) — `backend\app\models\activity.py`
- **TestCalcTransport** (16 connections) — `backend\tests\test_carbon_calculator.py`
- **calc_transport()** (13 connections) — `backend\app\services\carbon_calculator.py`
- **TestCalcFood** (12 connections) — `backend\tests\test_carbon_calculator.py`
- **TestCalcShopping** (10 connections) — `backend\tests\test_carbon_calculator.py`
- **calc_daily_total()** (9 connections) — `backend\app\services\carbon_calculator.py`
- **calc_food()** (9 connections) — `backend\app\services\carbon_calculator.py`
- **TestCalcEnergy** (9 connections) — `backend\tests\test_carbon_calculator.py`
- **TestCalcDailyTotal** (8 connections) — `backend\tests\test_carbon_calculator.py`
- **calc_shopping()** (7 connections) — `backend\app\services\carbon_calculator.py`
- **.test_full_day()** (7 connections) — `backend\tests\test_carbon_calculator.py`
- **carbon_calculator.py** (6 connections) — `backend\app\services\carbon_calculator.py`
- **test_carbon_calculator.py** (6 connections) — `backend\tests\test_carbon_calculator.py`
- **calc_energy()** (6 connections) — `backend\app\services\carbon_calculator.py`
- **Pure-function carbon emission calculator.  Every public function in this module** (5 connections) — `backend\app\services\carbon_calculator.py`
- **Calculate total CO₂ for shopping entries.      The emission factor is per ₹1 000** (5 connections) — `backend\app\services\carbon_calculator.py`
- **Calculate per-category and total CO₂ for a full day.      Args:         transpor** (5 connections) — `backend\app\services\carbon_calculator.py`
- **Calculate total CO₂ for a list of transport entries.      Args:         entries:** (5 connections) — `backend\app\services\carbon_calculator.py`
- **Calculate total CO₂ for a list of food entries.      Args:         entries: List** (5 connections) — `backend\app\services\carbon_calculator.py`
- **Calculate total CO₂ for energy-usage entries.      Args:         entries: List o** (5 connections) — `backend\app\services\carbon_calculator.py`
- **Unit tests for the pure-function carbon calculator.  These tests do not require** (5 connections) — `backend\tests\test_carbon_calculator.py`
- **3 chicken meals → 3 × 1.5 = 4.5 kg.** (5 connections) — `backend\tests\test_carbon_calculator.py`
- *... and 50 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\app\models\activity.py`
- `backend\app\services\carbon_calculator.py`
- `backend\tests\test_carbon_calculator.py`

## Audit Trail

- EXTRACTED: 155 (29%)
- INFERRED: 385 (71%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*