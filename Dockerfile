# BodmasParser Combined Dockerfile
# This Dockerfile builds both the Python API and serves the frontend via Nginx in a single container
FROM python:3.10-slim

# Install Nginx and required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy Nginx configuration
RUN mkdir -p /etc/nginx/sites-available/
COPY docker/nginx.combined.conf /etc/nginx/sites-available/default

# Set up directory for frontend files
RUN mkdir -p /var/www/html
COPY frontend/ /var/www/html/

# Configure the application
ENV DEBUG=False
ENV HOST=127.0.0.1
ENV API_PORT=8000
ENV FRONTEND_URL=https://bodmasparser.onrender.com

# Make script executable
RUN chmod +x /app/update_frontend_config.py

# Generate config files with internal API URL
ENV API_URL="/api"
RUN python /app/update_frontend_config.py

# Create a simple script to update the script.js file to use relative URLs
RUN echo '#!/bin/bash\necho "Updating script.js to use relative URLs"\nsed -i "s|const API_URL = window.BACKEND_URL .*|const API_URL = \"/api\";|g" /var/www/html/script.js\ncat /var/www/html/script.js | grep API_URL' > /app/update_script.sh && \
    chmod +x /app/update_script.sh && \
    /app/update_script.sh

# Copy supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the web port
EXPOSE 80

# Start supervisor which will manage Nginx and the Python API
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
