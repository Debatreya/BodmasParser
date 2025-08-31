# Contributing to BodmasParser

Thank you for your interest in contributing to the BodmasParser project! This document provides guidelines and instructions for setting up the project and contributing to its development.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Deployment Guidelines](#deployment-guidelines)
  - [Environment Configuration](#environment-configuration)
  - [Google Cloud Platform (GCP)](#deploying-on-google-cloud-platform-gcp)
  - [Render](#deploying-on-render)
  - [Heroku](#deploying-on-heroku)
- [CI/CD Setup](#cicd-setup)

## Getting Started

BodmasParser is a mathematical expression parser and visualizer that creates interactive parse trees for BODMAS/PEMDAS operations. The project consists of a Python backend API and a JavaScript frontend.

## Development Environment Setup

### Prerequisites
- Python 3.10 or higher
- Git
- A modern web browser

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BodmasParser.git
   cd BodmasParser
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - On Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure environment settings:
   ```bash
   # Review and edit the config.env file
   cat > config.env << EOL
   # BodmasParser Environment Configuration

   # Backend API URL (Used by the frontend to connect to the API)
   BACKEND_URL=http://127.0.0.1:8000

   # Frontend URL (Used by the backend for CORS configuration)
   FRONTEND_URL=http://127.0.0.1:8080

   # Server configuration
   API_PORT=8000
   FRONTEND_PORT=8080
   HOST=127.0.0.1

   # Debug mode (True/False)
   DEBUG=True
   EOL
   ```

## Project Structure

```
BodmasParser/
├── .venv/                  # Virtual environment (not committed)
├── assets/                 # Project images and static assets
├── frontend/               # Frontend HTML, CSS, and JavaScript files
│   ├── index.html          # Main application page
│   ├── script.js           # Frontend JavaScript
│   ├── styles.css          # CSS styles
│   ├── api.py              # FastAPI application for the backend
│   └── api-docs.html       # API documentation
├── tests/                  # Test files
├── __init__.py             # Package initialization
├── index.py                # Main parser implementation
├── operators.py            # Mathematical operators implementation
├── parseTree.py            # Parse tree generation and manipulation
├── config.env              # Environment configuration
├── requirements.txt        # Python dependencies
├── run_api.py              # Script to run the API server
└── serve_frontend.py       # Script to serve the frontend
```

## Running the Application

1. Start both servers with one command:
   ```bash
   ./start_servers.sh
   ```

   Alternatively, you can start them separately:

   ```bash
   # Terminal 1 - API server
   source .venv/bin/activate
   python run_api.py
   
   # Terminal 2 - Frontend server
   source .venv/bin/activate
   python serve_frontend.py
   ```

2. Access the application:
   - Frontend visualizer: http://localhost:8080
   - API documentation: http://localhost:8080/api-docs.html
   - API Swagger docs: http://localhost:8000/docs

## Testing

Run the test suite:

```bash
source .venv/bin/activate
pytest tests/
```

## Submitting Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git commit -m "Description of changes"
   ```

3. Push your changes and create a pull request.

## Style Guidelines

- Python code should follow PEP 8 standards
- JavaScript code should follow modern ES6+ practices
- Use descriptive variable and function names
- Comment complex sections of code
- Write tests for new functionality

## Deployment Guidelines

BodmasParser can be deployed on various cloud platforms. The following sections provide step-by-step guidelines for deploying the application to different environments.

### Docker Deployment

Docker provides a consistent environment across development and production. Here's how to containerize BodmasParser:

#### Create Docker Files

1. Create a `Dockerfile` for the API:

```dockerfile
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
```

2. Create a `Dockerfile.frontend` for the frontend:

```dockerfile
FROM nginx:alpine

# Copy frontend files
COPY frontend/ /usr/share/nginx/html/

# Configure nginx
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

3. Create the nginx configuration file:

```bash
mkdir -p docker
cat > docker/nginx.conf << EOL
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
EOL
```

4. Create a Docker Compose file:

```yaml
version: '3'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - HOST=0.0.0.0
      - API_PORT=8000
      - FRONTEND_URL=http://localhost:8080

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8080:80"
    depends_on:
      - api

```

#### Building and Running with Docker

```bash
# Build and run both services
docker-compose up --build

# Or build and run individual services
docker build -t bodmasparser-api .
docker build -t bodmasparser-frontend -f Dockerfile.frontend .
docker run -p 8000:8000 bodmasparser-api
docker run -p 8080:80 bodmasparser-frontend
```

### General Deployment Considerations

Before deploying to any platform:

1. Update the configuration in `config.env`:
   ```
   # Set production URLs
   BACKEND_URL=https://your-backend-domain.com
   FRONTEND_URL=https://your-frontend-domain.com
   
   # Turn off debug mode
   DEBUG=False
   ```

2. Generate a production config.json file:
   ```bash
   source .venv/bin/activate
   python generate_config.py
   ```

3. Test the application locally with production settings before deploying.

### Deploying on Google Cloud Platform (GCP)

#### Backend API Deployment (Cloud Run)

1. Install and set up Google Cloud CLI:
   ```bash
   # Install gcloud CLI and login
   gcloud auth login
   gcloud config set project your-project-id
   ```

2. Build and deploy the API to Cloud Run:
   ```bash
   # Create Dockerfile for API
   cat > Dockerfile.api << EOL
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   ENV PORT=8080
   CMD ["python", "run_api.py"]
   EOL
   
   # Build and deploy
   gcloud builds submit --tag gcr.io/your-project-id/bodmasparser-api
   gcloud run deploy bodmasparser-api --image gcr.io/your-project-id/bodmasparser-api --platform managed --allow-unauthenticated
   ```

3. Note the URL provided after deployment for use in the frontend configuration.

#### Frontend Deployment (Cloud Storage + Cloud CDN)

1. Prepare the frontend files:
   ```bash
   # Update config.json with the backend URL from Cloud Run
   echo '{
     "BACKEND_URL": "https://bodmasparser-api-xxxx-run.app",
     "VERSION": "1.0.0",
     "DEBUG": false
   }' > frontend/config.json
   ```

2. Deploy to Cloud Storage:
   ```bash
   # Create a storage bucket
   gsutil mb gs://bodmasparser-frontend
   
   # Upload files
   gsutil -m cp -r frontend/* gs://bodmasparser-frontend/
   
   # Make the bucket public
   gsutil iam ch allUsers:objectViewer gs://bodmasparser-frontend
   ```

3. Set up Cloud CDN (optional):
   ```bash
   # Create a load balancer with CDN
   gcloud compute backend-buckets create bodmasparser-backend --gcs-bucket-name=bodmasparser-frontend --enable-cdn
   
   # Set up URL map and forwarding rules (simplified)
   # Follow GCP documentation for detailed steps
   ```

### Deploying on Render

#### Backend API Deployment

1. Create a new Web Service on Render:
   - Connect your GitHub repository
   - Set Build Command: `pip install -r requirements.txt`
   - Set Start Command: `uvicorn frontend.api:app --host 0.0.0.0 --port $PORT`
   - Add the environment variables from your `config.env` file

2. After deployment, note the service URL for the frontend configuration.

#### Frontend Deployment

1. Create a new Static Site on Render:
   - Connect your GitHub repository
   - Set Publish Directory: `frontend`
   - Add an environment variable: `BACKEND_URL=https://bodmasparser-api.onrender.com` (use your actual API URL)
   - Add a Build Command:
     ```bash
     echo '{
       "BACKEND_URL": "'"$BACKEND_URL"'",
       "VERSION": "1.0.0",
       "DEBUG": false
     }' > frontend/config.json
     ```

2. After deployment, your frontend will be accessible at the provided Render URL.

### Deploying on Heroku

#### Backend API Deployment

1. Create a `Procfile` in the project root:
   ```
   web: uvicorn frontend.api:app --host=0.0.0.0 --port=$PORT
   ```

2. Create a new Heroku app and deploy:
   ```bash
   # Install Heroku CLI and login
   heroku login
   
   # Create app
   heroku create bodmasparser-api
   
   # Set environment variables
   heroku config:set DEBUG=False
   heroku config:set FRONTEND_URL=https://bodmasparser-frontend.herokuapp.com
   
   # Deploy
   git push heroku main
   ```

#### Frontend Deployment

1. Create a separate Heroku app for the frontend:
   ```bash
   heroku create bodmasparser-frontend
   ```

2. Set up a simple Express server to serve the static files:
   ```bash
   # Create server.js
   cat > server.js << EOL
   const express = require('express');
   const path = require('path');
   const app = express();
   
   // Generate config.json with environment variables
   const fs = require('fs');
   const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
   const config = {
     BACKEND_URL: backendUrl,
     VERSION: '1.0.0',
     DEBUG: false
   };
   fs.writeFileSync(path.join(__dirname, 'frontend', 'config.json'), JSON.stringify(config, null, 2));
   
   // Serve static files
   app.use(express.static('frontend'));
   
   // Start server
   const PORT = process.env.PORT || 8080;
   app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
   EOL
   
   # Create package.json
   cat > package.json << EOL
   {
     "name": "bodmasparser-frontend",
     "version": "1.0.0",
     "main": "server.js",
     "dependencies": {
       "express": "^4.17.1"
     },
     "scripts": {
       "start": "node server.js"
     }
   }
   EOL
   
   # Set environment variables
   heroku config:set BACKEND_URL=$(heroku info -s -a bodmasparser-api | grep web_url | cut -d= -f2 | tr -d '/')
   
   # Deploy
   git push heroku main
   ```

## CI/CD Setup

Setting up Continuous Integration and Deployment will help automate testing and deployment. Here are sample configurations for popular CI/CD platforms.

### GitHub Actions

Create a file `.github/workflows/main.yml` in your repository:

```yaml
name: BodmasParser CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/

  deploy-api:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      # Add deployment steps for your chosen platform
      # Example for GCP Cloud Run:
      - uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v1
        with:
          service: bodmasparser-api
          source: .
          # Add other required parameters

  deploy-frontend:
    needs: deploy-api
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      # Add frontend deployment steps
      # Example for GCP Storage:
      - name: Generate config.json
        run: |
          echo '{
            "BACKEND_URL": "${{ secrets.BACKEND_URL }}",
            "VERSION": "1.0.0",
            "DEBUG": false
          }' > frontend/config.json
      # Add deployment steps for your frontend
```

### GitLab CI/CD

Create a `.gitlab-ci.yml` file in your repository:

```yaml
stages:
  - test
  - deploy-api
  - deploy-frontend

test:
  stage: test
  image: python:3.10
  script:
    - pip install -r requirements.txt
    - pytest tests/

deploy-api:
  stage: deploy-api
  image: google/cloud-sdk:latest
  script:
    - echo $GCP_SA_KEY > gcp-key.json
    - gcloud auth activate-service-account --key-file gcp-key.json
    - gcloud config set project $GCP_PROJECT_ID
    - gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/bodmasparser-api
    - gcloud run deploy bodmasparser-api --image gcr.io/$GCP_PROJECT_ID/bodmasparser-api --platform managed --allow-unauthenticated
  only:
    - main

deploy-frontend:
  stage: deploy-frontend
  image: google/cloud-sdk:latest
  script:
    - echo '{
        "BACKEND_URL": "'$BACKEND_URL'",
        "VERSION": "1.0.0",
        "DEBUG": false
      }' > frontend/config.json
    - gsutil -m cp -r frontend/* gs://$GCS_BUCKET/
  only:
    - main
```

## Environment Configuration for Production

When deploying to production, you should consider the following environment variables in your `config.env` file:

```
# Backend and Frontend URLs
BACKEND_URL=https://api.yourdomain.com
FRONTEND_URL=https://yourdomain.com

# Server configuration
API_PORT=8000
HOST=0.0.0.0  # Listen on all interfaces in production

# Security settings (add these for production)
API_KEY=your-secure-api-key
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
RATE_LIMIT_PER_MINUTE=100

# Debug and logging
DEBUG=False
LOG_LEVEL=INFO

# Optional: Database configuration if you add one
# DB_CONNECTION_STRING=postgresql://user:password@localhost/dbname
```

## Future Development Opportunities

- Support for additional mathematical operators
- User accounts to save expressions
- Mobile app version
- Step-by-step evaluation animation
- Expression history tracking
- Expression sharing capabilities
- Integration with educational platforms
- Mobile app development
- Adding support for more complex mathematical functions
- Creating a public API for third-party integrations
