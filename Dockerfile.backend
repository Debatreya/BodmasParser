# BodmasParser API Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Configure the application
ENV DEBUG=False
ENV HOST=0.0.0.0
ENV API_PORT=8000
ENV FRONTEND_URL=http://localhost:8080

# Generate config files
RUN python generate_config.py

# Expose the API port
EXPOSE 8000

# Run the API server
CMD ["python", "run_api.py"]
