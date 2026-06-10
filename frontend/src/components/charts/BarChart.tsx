/**
 * @fileoverview Weekly comparison bar chart using Chart.js with dark theme.
 * Displays this week vs last week CO2 emissions.
 */
import React, { useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  type ChartOptions,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import type { WeeklyDataPoint } from '@/types';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface BarChartProps {
  /** Weekly comparison data points */
  data: WeeklyDataPoint[];
  /** Chart height */
  height?: number;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Weekly comparison bar chart with dark theme styling.
 * Shows this week vs last week CO2 emissions side by side.
 * @param props - BarChart properties including data and height
 */
const BarChart = React.memo<BarChartProps>(function BarChart({
  data,
  height = 220,
  className = '',
}) {
  const chartData = useMemo(
    () => ({
      labels: data.map((d) => d.day),
      datasets: [
        {
          label: 'This Week',
          data: data.map((d) => d.thisWeek),
          backgroundColor: 'rgba(22, 163, 74, 0.8)',
          borderColor: 'rgba(22, 163, 74, 1)',
          borderWidth: 1,
          borderRadius: 6,
          borderSkipped: false as const,
        },
        {
          label: 'Last Week',
          data: data.map((d) => d.lastWeek),
          backgroundColor: 'rgba(100, 116, 139, 0.4)',
          borderColor: 'rgba(100, 116, 139, 0.6)',
          borderWidth: 1,
          borderRadius: 6,
          borderSkipped: false as const,
        },
      ],
    }),
    [data],
  );

  const options = useMemo<ChartOptions<'bar'>>(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top' as const,
          align: 'end' as const,
          labels: {
            color: 'rgba(148, 163, 184, 1)',
            font: { family: 'Inter', size: 11 },
            boxWidth: 12,
            boxHeight: 12,
            borderRadius: 3,
            useBorderRadius: true,
            padding: 16,
          },
        },
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
            label: (context) =>
              ` ${context.dataset.label}: ${(context.parsed.y ?? 0).toFixed(1)} kg CO₂`,
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            color: 'rgba(148, 163, 184, 0.7)',
            font: { family: 'Inter', size: 11 },
          },
          border: { display: false },
        },
        y: {
          grid: {
            color: 'rgba(148, 163, 184, 0.08)',
          },
          ticks: {
            color: 'rgba(148, 163, 184, 0.7)',
            font: { family: 'Inter', size: 11 },
            callback: (value) => `${value}`,
          },
          border: { display: false },
        },
      },
    }),
    [],
  );

  return (
    <div
      className={`w-full ${className}`}
      style={{ height }}
      role="img"
      aria-label="Weekly CO2 emissions comparison bar chart"
    >
      <Bar data={chartData} options={options} />
    </div>
  );
});

export default BarChart;
