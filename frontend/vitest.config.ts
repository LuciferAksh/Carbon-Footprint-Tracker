import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        statements: 65,
        branches: 60,
        functions: 60,
        lines: 65,
      },
      exclude: [
        'node_modules/**',
        'src/test/**',
        'vite.config.ts',
        'vitest.config.ts',
        'src/main.tsx',
        'src/vite-env.d.ts',
        'src/**/index.ts',
        'src/components/layout/AppShell.tsx',
        'src/features/onboarding/ProfileResult.tsx',
        'src/features/profile/ProfileScreen.tsx',
        'src/features/reports/MonthlyReport.tsx',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
