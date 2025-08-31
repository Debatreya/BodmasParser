#!/usr/bin/env python3
"""
Serves the frontend static files using Python's built-in HTTP server
"""

import http.server
import socketserver
import os
import dotenv

# Load environment variables from config.env
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.env"))

# Change directory to frontend
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
os.chdir(frontend_dir)

# Set port from environment or use default
HOST = os.getenv("HOST", "")  # Empty string means all available interfaces
PORT = int(os.getenv("FRONTEND_PORT", 8080))

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((HOST, PORT), handler) as httpd:
    print(f"Frontend server started at http://{HOST or 'localhost'}:{PORT}")
    print(f"Serving files from: {frontend_dir}")
    print("Press Ctrl+C to stop the server")
    httpd.serve_forever()
