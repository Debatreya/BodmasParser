#!/usr/bin/env python3
"""
Serves the frontend static files using Python's built-in HTTP server
"""

import http.server
import socketserver
import os

# Change directory to frontend
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend'))

# Set port
PORT = 8080

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Server started at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    httpd.serve_forever()
