#!/usr/bin/env python3
"""
Test script to verify API connectivity within the container
"""

import time
import requests
import sys
import os

def main():
    # Wait for services to start
    print("Waiting for services to start...")
    time.sleep(5)
    
    # Test internal API
    try:
        response = requests.get("http://127.0.0.1:8000/ping")
        print(f"Internal API test: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Internal API test failed: {e}")
        
    # Test external API route
    try:
        response = requests.get("http://localhost/api/ping")
        print(f"External API route test: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"External API route test failed: {e}")
    
    # Print environment variables
    print("\nEnvironment Variables:")
    print(f"API_PORT: {os.environ.get('API_PORT', '8000')}")
    print(f"FRONTEND_URL: {os.environ.get('FRONTEND_URL', 'not set')}")
    print(f"DEBUG: {os.environ.get('DEBUG', 'not set')}")
    
    print("\nAPI test completed")

if __name__ == "__main__":
    main()
