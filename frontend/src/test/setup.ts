/**
 * @fileoverview Vitest test setup — provides browser API mocks
 * (matchMedia, ResizeObserver, IntersectionObserver, scrollTo)
 * required by Framer Motion, Chart.js, and other UI libraries.
 */
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock matchMedia (used by Framer Motion / reduced motion hook)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock ResizeObserver (used by Chart.js / responsiveness)
class MockResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}
window.ResizeObserver = MockResizeObserver;

// Mock IntersectionObserver
class MockIntersectionObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}
window.IntersectionObserver = MockIntersectionObserver as any;

// Mock window.scrollTo
window.scrollTo = vi.fn();
