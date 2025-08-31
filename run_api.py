#!/usr/bin/env python3
"""
Launches the FastAPI server for the BodmasParser API
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "frontend.api:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,
        reload=True  # Auto-reload when code changes (development only)
    )
