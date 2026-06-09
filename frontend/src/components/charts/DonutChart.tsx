/**
 * @fileoverview Category breakdown donut chart using Chart.js with dark theme.
 * Displays CO2 distribution across categories with center text.
 */
import React, { useMemo } from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  type ChartOptions,
} from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import type { CategoryBreakdown } from '@/types';

ChartJS.register(ArcElement, Tooltip, Legend);

interface DonutChartProps {
  /** Category breakdown data */
  data: CategoryBreakdown[];
  /** Center label text */
  centerLabel?: string;
  /** Center value text */
  centerValue?: string;
  /** Chart size */
  size?: number;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Donut chart for category breakdown with dark theme.
 * Shows proportional CO2 distribution with an optional center overlay.
 * @param props - DonutChart properties including data, center text, and size
 */
const DonutChart = React.memo<DonutChartProps>(function DonutChart({
  data,
  centerLabel,
  centerValue,
  size = 200,
  className = '',
}) {
  const chartData = useMemo(
    () => ({
      labels: data.map((d) => d.category.charAt(0).toUpperCase() + d.category.slice(1)),
      datasets: [
        {
          data: data.map((d) => d.amount),
          backgroundColor: data.map((d) => d.color),
          borderColor: 'rgba(15, 23, 42, 0.8)',
          borderWidth: 3,
          hoverBorderWidth: 0,
          hoverOffset: 8,
        },
      ],
    }),
    [data],
  );

  const options = useMemo<ChartOptions<'doughnut'>>(
    () => ({
      responsive: true,
      maintainAspectRatio: true,
      cutout: '70%',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          titleColor: '#f1f5f9',
          bodyColor: '#94a3b8',
          borderColor: 'rgba(148, 163, 184, 0.2)',
          borderWidth: 1,
          cornerRadius: 12,
          padding: 12,
          titleFont: { family: 'Inter', weight: 600 as const },
          bodyFont: { family: 'Inter' },
          callbacks: {
            label: (context) => {
              const value = context.parsed;
              const total = data.reduce((sum, d) => sum + d.amount, 0);
              const pct = total > 0 ? ((value / total) * 100).toFixed(1) : '0';
              return ` ${context.label}: ${value.toFixed(1)} kg (${pct}%)`;
            },
          },
        },
      },
    }),
    [data],
  );

  return (
    <div
      className={`relative inline-flex items-center justify-center ${className}`}
      style={{ width: size, height: size }}
      role="img"
      aria-label="Carbon emissions category breakdown donut chart"
    >
      <Doughnut data={chartData} options={options} />
      {(centerLabel || centerValue) && (
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          {centerValue && (
            <span className="text-2xl font-bold text-dark-100">{centerValue}</span>
          )}
          {centerLabel && (
            <span className="text-xs text-dark-400 mt-0.5">{centerLabel}</span>
          )}
        </div>
      )}
    </div>
  );
});

export default DonutChart;
