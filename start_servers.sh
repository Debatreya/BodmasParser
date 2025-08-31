#!/bin/bash
# Script to start both the API and frontend servers

echo "Starting BodmasParser API and Frontend..."

# Kill any existing instances
pkill -f "python run_api.py" 2>/dev/null
pkill -f "python serve_frontend.py" 2>/dev/null

# Move to the project directory
cd "$(dirname "$0")"

# Generate config files from environment variables
echo "Generating configuration files..."
source .venv/bin/activate
python generate_config.py

# Start the API server in the background
echo "Starting API server..."
python run_api.py > /dev/null 2>&1 &
API_PID=$!

# Wait a moment to ensure API is up
sleep 2

# Check if API is running
if ! curl -s http://127.0.0.1:8000/ping > /dev/null; then
    echo "Error: API server failed to start. Check api_server.log for details."
    exit 1
fi

echo "API server started with PID $API_PID"

# Start the frontend server in the background
echo "Starting frontend server..."
python serve_frontend.py > /dev/null 2>&1 &
FRONTEND_PID=$!

echo "Frontend server started with PID $FRONTEND_PID"
echo "Frontend available at: http://localhost:8080"
echo "API available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "Or use 'pkill -f \"python run_api.py\"' and 'pkill -f \"python serve_frontend.py\"' to stop them individually"

# Wait for Ctrl+C
trap "echo 'Stopping servers...'; kill $API_PID $FRONTEND_PID 2>/dev/null" INT
wait
