#!/usr/bin/env python3
"""
Script to generate frontend configuration from environment variables
This enables the frontend to use the same configuration as the backend
"""

import os
import json
import dotenv
import sys
from pathlib import Path

# Get the project root directory
project_dir = Path(__file__).parent
frontend_dir = project_dir / "frontend"

def main():
    # Load environment variables from config.env
    dotenv.load_dotenv(project_dir / "config.env")
    
    # Extract the relevant configuration values
    config = {
        "BACKEND_URL": os.getenv("BACKEND_URL", "http://127.0.0.1:8000"),
        "VERSION": "1.0.0",
        "DEBUG": os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    }
    
    # Write to the JSON file
    config_path = frontend_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"Configuration written to {config_path}")

if __name__ == "__main__":
    main()
