# Deployment Guide - "My First API"

This comprehensive guide provides instructions for setting up, developing, and deploying the FastAPI application in various environments.

> **Project**: My First API  
> **Framework**: FastAPI  
> **Python Version**: 3.12+  
> **Last Updated**: 2026-02-26

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Local Development Setup](#2-local-development-setup)
3. [Running the Application](#3-running-the-application)
4. [Docker Deployment](#4-docker-deployment)
5. [Platform as a Service (PaaS)](#5-platform-as-a-service-paas)
6. [Cloud Platform Deployment](#6-cloud-platform-deployment)
7. [Environment Configuration](#7-environment-configuration)
8. [Production Best Practices](#8-production-best-practices)
9. [CI/CD Pipeline](#9-cicd-pipeline)
10. [Troubleshooting](#10-troubleshooting)
11. [Helpful Commands](#11-helpful-commands)

---

## 1. Prerequisites

### 1.1 Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.12 or higher | Runtime environment |
| **pip** | Latest | Package manager |
| **git** | Latest | Version control |

### 1.2 Installing Python

#### macOS
```bash
# Using Homebrew (recommended)
brew install python3.12

# Verify installation
python3.12 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

# Verify installation
python3.12 --version
```

#### Windows
- Download from [python.org](https://www.python.org/downloads/)
- Or use [Windows Package Manager](https://learn.microsoft.com/en-us/windows/package-manager/): `winget install Python.3.12`

---

## 2. Local Development Setup

### 2.1 Clone the Repository

```bash
# Navigate to your projects directory
cd /path/to/your/projects

# Clone or navigate to the project
git clone <your-repo-url> Flask_Quick_start
cd Flask_Quick_start
```

### 2.2 Create Virtual Environment

#### Option A: Using the Existing Virtual Environment
The project already contains a pre-configured virtual environment folder `teja` in the `backend` directory.

```bash
# Navigate to the backend directory
cd backend

# Activate the virtual environment
# On macOS/Linux:
source teja/bin/activate

# On Windows:
teja\Scripts\activate

# Verify you're in the virtual environment
# You should see (teja) at the beginning of your terminal prompt
which python  # Should show path to teja/bin/python
```

#### Option B: Creating a New Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create a new virtual environment
python3.12 -m venv myenv

# Activate the virtual environment
# On macOS/Linux:
source myenv/bin/activate

# On Windows:
myenv\Scripts\activate

# Upgrade pip to latest version
pip install --upgrade pip
```

### 2.3 Install Dependencies

```bash
# Install core dependencies
pip install fastapi uvicorn

# Or install with all optional dependencies
pip install "fastapi[all]"  # Includes uvicorn, pydantic, etc.

# For production, install just the essentials
pip install fastapi uvicorn[standard]
```

### 2.4 Create requirements.txt

```bash
# Freeze dependencies to requirements.txt
pip freeze > requirements.txt

# Or create a requirements file with specific versions
cat > requirements.txt << EOF
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
EOF
```

---

## 3. Running the Application

### 3.1 Development Mode (with auto-reload)

```bash
# Navigate to backend directory
cd backend

# Run with auto-reload (recommended for development)
uvicorn main:app --reload

# Or specify host and port
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3.2 Access Points

| Service | URL |
|---------|-----|
| **API Base URL** | http://127.0.0.1:8000 |
| **Interactive Docs (Swagger UI)** | http://127.0.0.1:8000/docs |
| **Alternative Docs (ReDoc)** | http://127.0.0.1:8000/redoc |
| **OpenAPI Schema (JSON)** | http://127.0.0.1:8000/openapi.json |
| **Health Check** | http://127.0.0.1:8000/ |

### 3.3 Test the Endpoints

```bash
# Test root endpoint
curl http://127.0.0.1:8000/
# Response: {"message":"Hello, FastAPI!"}

# Test greeting endpoint
curl "http://127.0.0.1:8000/greet/John"
# Response: {"greeting":"greeted, John"}

# Test excited greeting
curl "http://127.0.0.1:8000/greet/John?excited=true"
# Response: {"greeting":"greeted, John!!!"}

# Test status endpoint
curl http://127.0.0.1:8000/api/status
# Response: {"status":"running","framework":"FastAPI","docs":"/docs"}
```

---

## 4. Docker Deployment

### 4.1 Why Docker?

- **Consistency**: Same environment across development and production
- **Isolation**: No dependency conflicts
- **Portability**: Run anywhere Docker is installed

### 4.2 Create Dockerfile

Create a `Dockerfile` in the `backend` directory:

```dockerfile
# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.3 Create .dockerignore

Create a `.dockerignore` file in the `backend` directory:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.pytest_cache/

# Git
.git/
.gitignore

# IDE
.vscode/
.idea/
*.swp
*.swo

# Local environment
teja/
*.db
*.log

# Docker
Dockerfile
docker-compose.yml
```

### 4.4 Build and Run Docker Container

```bash
# Navigate to backend directory
cd backend

# Build the Docker image
docker build -t my-first-api:latest .

# Run the container
docker run -d \
  --name my-first-api \
  -p 8000:8000 \
  my-first-api:latest

# Check if container is running
docker ps

# View logs
docker logs -f my-first-api

# Stop the container
docker stop my-first-api
```

### 4.5 Docker Compose (Recommended for Development)

Create a `docker-compose.yml` file in the `backend` directory:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=true
    volumes:
      - .:/app
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    restart: unless-stopped

  # Optional: Add a reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
    restart: unless-stopped
```

Run with Docker Compose:
```bash
cd backend
docker-compose up --build
```

---

## 5. Platform as a Service (PaaS)

### 5.1 Render

1. **Connect GitHub Repository**
   - Create a Render account
   - Connect your GitHub repository

2. **Create a Web Service**
   - New → Web Service
   - Select your repository
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   - Add any required environment variables in Render dashboard

### 5.2 Railway

1. **Deploy from GitHub**
   - Create a Railway project
   - Connect your GitHub repository

2. **Configure Settings**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `backend`

3. **Deploy**
   - Railway automatically detects Python and FastAPI

### 5.3 Fly.io

```bash
# Install flyctl
brew install flyctl

# Login
fly auth login

# Launch
fly launch

# Configure the app (update fly.toml)
# Set the following in your Dockerfile or fly.toml:
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# Deploy
fly deploy
```

---

## 6. Cloud Platform Deployment

### 6.1 AWS App Runner

1. **Create repository** in Amazon ECR
2. **Push Docker image** to ECR
3. **Create App Runner service**
   - Image repository: Your ECR repository
   - Port: `8000`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 8080`

### 6.2 Google Cloud Run

```bash
# Install Google Cloud SDK
brew install google-cloud-sdk

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy my-first-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

### 6.3 Azure Container Apps

```bash
# Install Azure CLI
brew install azure-cli

# Login
az login

# Create container registry
az acr create --resource-group my-rg --name myregistry --sku Basic

# Build and push
az acr build --registry myregistry --image my-first-api:latest .

# Deploy to Container Apps
az containerapp create \
  --name my-first-api \
  --resource-group my-rg \
  --image myregistry.azurecr.io/my-first-api:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 0.25 --memory 0.5Gi
```

---

## 7. Environment Configuration

### 7.1 Using Environment Variables

Create a `.env` file (add to `.gitignore`):

```bash
# .env
DEBUG=true
LOG_LEVEL=debug
API_TITLE="My First API"
API_VERSION=1.0.0
```

### 7.2 Loading Environment Variables in FastAPI

Update `main.py` to use environment variables:

```python
# main.py
import os
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My First API"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
```

Install pydantic-settings:
```bash
pip install pydantic-settings
```

---

## 8. Production Best Practices

### 8.1 Security Checklist

- [ ] Use HTTPS/TLS (required in production)
- [ ] Set `debug=False` in production
- [ ] Configure CORS for allowed origins only
- [ ] Implement authentication (API keys, JWT)
- [ ] Add rate limiting
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets

### 8.2 Performance Checklist

- [ ] Use `uvicorn[standard]` for production (includes Gunicorn)
- [ ] Run behind a reverse proxy (Nginx, Traefik)
- [ ] Implement caching if needed
- [ ] Add connection pooling for database
- [ ] Use async/await for I/O operations
- [ ] Configure proper timeout settings

### 8.3 Logging & Monitoring

```python
# Add structured logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello, FastAPI!"}
```

### 8.4 Production Uvicorn Command

```bash
# Using uvicorn directly (single worker)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or with Gunicorn (recommended)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

---

## 9. CI/CD Pipeline

### 9.1 GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          
      - name: Run tests
        run: |
          cd backend
          pip install pytest httpx
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to Render
        uses: render-examples/github-actions@v1
        with:
          api_key: ${{ secrets.RENDER_API_KEY }}
          service_id: ${{ secrets.RENDER_SERVICE_ID }}
```

---

## 10. Troubleshooting

### 10.1 Common Issues

| Issue | Solution |
|-------|----------|
| **Port already in use** | Kill existing process: `lsof -ti:8000 \| xargs kill` or use different port |
| **Module not found** | Activate virtual environment and reinstall dependencies |
| **Permission denied** | Check file permissions or run with appropriate user |
| **Docker build fails** | Check Python version compatibility and requirements.txt |
| **Import errors** | Ensure you're in the correct directory (backend/) |

### 10.2 Debug Mode

```bash
# Enable verbose logging
uvicorn main:app --log-level debug --reload

# Or in Python code:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 10.3 Check Python Path

```bash
# Verify Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check if main.py can be imported
cd backend
python -c "import main; print(main.app)"
```

---

## 11. Helpful Commands

### Development Commands

```bash
# Activate virtual environment
source backend/teja/bin/activate

# Run development server with auto-reload
cd backend && uvicorn main:app --reload

# Run with specific port
cd backend && uvicorn main:app --port 9000 --reload

# Check installed packages
pip list

# Freeze dependencies
pip freeze > requirements.txt

# Deactivate virtual environment
deactivate
```

### Docker Commands

```bash
# Build image
docker build -t my-first-api backend/

# Run container
docker run -p 8000:8000 my-first-api

# Run in background
docker run -d -p 8000:8000 --name my-api my-first-api

# View logs
docker logs my-api

# Access container shell
docker exec -it my-api sh

# Remove container and image
docker rm my-api && docker rmi my-first-api
```

### API Testing Commands

```bash
# Test with curl
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/greet/World
curl http://127.0.0.1:8000/greet/World?excited=true
curl http://127.0.0.1:8000/api/status

# Test with HTTPie (recommended)
http http://127.0.0.1:8000/
http http://127.0.0.1:8000/greet/World excited==true

# Install HTTPie
pip install httpie
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| **Start Development Server** | `cd backend && uvicorn main:app --reload` |
| **Run Tests** | `pytest` |
| **Build Docker** | `docker build -t my-first-api backend/` |
| **Run Docker** | `docker run -p 8000:8000 my-first-api` |
| **Install Dependencies** | `pip.txt` |
| **Create requirements install -r requirements.txt** | `pip freeze > requirements.txt` |

---

## Support & Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Uvicorn Documentation**: https://www.uvicorn.org/
- **Docker Documentation**: https://docs.docker.com/
- **Render Deployment**: https://render.com/docs/deploy-fastapi

---

**Document Version**: 1.1  
**Last Updated**: 2026-02-26
