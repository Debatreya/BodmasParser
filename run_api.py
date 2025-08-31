#!/usr/bin/env python3
"""
Launches the FastAPI server for the BodmasParser API
"""

import os
import uvicorn
import dotenv

# Load environment variables from config.env
dotenv.load_dotenv("config.env")

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    
    print(f"Starting API server on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    uvicorn.run(
        "frontend.api:app",
        host=host,
        port=port,
        reload=debug  # Auto-reload only in debug mode
    )
