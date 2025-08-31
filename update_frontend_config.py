#!/usr/bin/env python3
"""
Script to update frontend config.json with the correct API URL
This is especially useful for deployment environments
"""

import os
import json
import sys
from pathlib import Path

def main():
    # Get base directory
    base_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    
    # Set paths
    config_path = base_dir / "frontend" / "config.json"
    www_config_path = Path("/var/www/html/config.json")
    
    # Use the config path that exists
    if www_config_path.exists():
        config_path = www_config_path
    
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)
    
    # Read current config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Get environment variables or use defaults
    api_url = os.getenv('API_URL', '/api')
    version = os.getenv('VERSION', '1.0.0')
    debug = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
    
    # Update config
    config['BACKEND_URL'] = api_url
    config['VERSION'] = version
    config['DEBUG'] = debug
    
    # Write updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Updated config at {config_path} with BACKEND_URL={api_url}")

if __name__ == "__main__":
    main()
