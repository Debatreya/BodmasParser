// This script loads configuration settings from the backend
// It must be loaded before the main script.js

// Function to fetch configuration from the backend
async function loadConfiguration() {
  try {
    // Try to load config from the server
    const response = await fetch('/config.json');
    if (response.ok) {
      const config = await response.json();
      
      // Set global configuration
      window.BACKEND_URL = config.BACKEND_URL || window.BACKEND_URL;
      console.log('Configuration loaded:', { BACKEND_URL: window.BACKEND_URL });
    } else {
      console.warn('Failed to load configuration, using defaults');
    }
  } catch (error) {
    console.warn('Error loading configuration, using defaults:', error);
  }
}

// Initialize default configuration
window.BACKEND_URL = 'http://127.0.0.1:8000';

// Try to load configuration, but don't block page load
loadConfiguration().catch(error => {
  console.warn('Configuration load error:', error);
});
