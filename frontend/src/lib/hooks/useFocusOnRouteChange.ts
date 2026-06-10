import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

/**
 * Custom hook to manage keyboard focus on route transitions.
 * Finds the element with id="main-content", sets its tabIndex to -1 if needed,
 * and programmatically focuses it. This ensures screen readers announce the
 * new page content and keyboard navigation starts at the beginning of the page.
 */
export function useFocusOnRouteChange(): void {
  const { pathname } = useLocation();

  useEffect(() => {
    // Find the main content container
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      // Set tabIndex to -1 so it is programmatically focusable but not in tab order
      if (mainContent.getAttribute('tabindex') === null) {
        mainContent.setAttribute('tabindex', '-1');
      }
      
      // Focus the container
      mainContent.focus();
    }
  }, [pathname]);
}
