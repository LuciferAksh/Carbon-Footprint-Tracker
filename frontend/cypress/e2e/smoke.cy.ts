describe('CarbonCoach E2E Smoke Test', () => {
  beforeEach(() => {
    // Clear localStorage to ensure we are logged out before test
    cy.clearLocalStorage();
  });

  it('allows logging in as a guest and navigating the app', () => {
    // 1. Visit the root URL
    cy.visit('/');

    // 2. We should be redirected to /login
    cy.url().should('include', '/login');
    cy.contains('CarbonCoach').should('be.visible');

    // 3. Click the guest sign-in button
    cy.contains('Explore as Guest (Demo Mode)').should('be.visible').click();

    // 4. We should be logged in and redirected
    // If onboarding is incomplete, it goes to /onboarding
    cy.url().then((url) => {
      if (url.includes('/onboarding')) {
        // Step 1: Location
        cy.contains('Where are you located?').should('be.visible');
        cy.contains('India').click();
        cy.contains('Continue').click();
        
        // Step 2: Household Size
        cy.contains('How big is your household?').should('be.visible');
        cy.get('[aria-label="Increase count"]').click(); // increases to 2
        cy.contains('Continue').click();
        
        // Step 3: Transport
        cy.contains('Your primary transport?').should('be.visible');
        cy.contains('Electric Car').click();
        cy.contains('Continue').click();
        
        // Step 4: Diet
        cy.contains("What's your typical diet?").should('be.visible');
        cy.contains('Vegetarian').click();
        cy.contains('Continue').click();
        
        // Step 5: Energy
        cy.contains('Your energy source?').should('be.visible');
        cy.contains('Grid Electricity').click();
        cy.contains('Continue').click();
        
        // Step 6: Shopping
        cy.contains('Shopping habits?').should('be.visible');
        cy.contains('Moderate').click();
        cy.contains('See My Profile').click();

        // View profile results
        cy.contains('Your Carbon Profile', { timeout: 10000 }).should('be.visible');
        cy.contains('Start Tracking').click();
      }
      
      // We should be on the dashboard (root /)
      cy.url().should('match', /\/$/);
      cy.contains('My Carbon Story').should('be.visible');

      // Navigate to Log screen
      cy.get('nav').within(() => {
        cy.contains('Log').click();
      });
      cy.url().should('include', '/log');
      cy.contains('Log Activity').should('be.visible');

      // Navigate to Coach screen
      cy.get('nav').within(() => {
        cy.contains('Coach').click();
      });
      cy.url().should('include', '/coach');
      cy.contains('CarbonCoach AI').should('be.visible');

      // Navigate to Challenges screen
      cy.get('nav').within(() => {
        cy.contains('Challenges').click();
      });
      cy.url().should('include', '/challenges');
      cy.contains("This Week's Mission").should('be.visible');

      // Navigate to Profile screen
      cy.get('nav').within(() => {
        cy.contains('Profile').click();
      });
      cy.url().should('include', '/profile');
      cy.contains('Carbon Score').should('be.visible');
    });
  });
});
