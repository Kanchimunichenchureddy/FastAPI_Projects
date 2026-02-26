# Deployment Guide - "Async API Aggregator"

This comprehensive guide provides instructions for setting up, developing, and deploying the Async API Aggregator with concurrent processing and caching.

> **Project**: Async API Aggregator  
> **Framework**: FastAPI  
> **Features**: Async Aggregation, TTL Caching  
> **Python Version**: 3.12+  
> **Last Updated**: 2026-02-26

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Local Development Setup](#2-local-development-setup)
3. [API Keys Configuration](#3-api-keys-configuration)
4. [Running the Application](#4-running-the-application)
5. [API Testing](#5-api-testing)
6. [Docker Deployment](#6-docker-deployment)
7. [Cloud Platform Deployment](#7-cloud-platform-deployment)
8. [Production Best Practices](#8-production-best-practices)
9. [Performance Optimization](#9-performance-optimization)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.12 or higher | Runtime environment |
| **pip** | Latest | Package manager |
| **git** | Latest | Version control |

### 1.2 Optional: External API Accounts

| Service | Purpose | Signup URL |
|---------|---------|------------|
| OpenWeatherMap | Weather data | https://openweathermap.org/api |
| NewsAPI | News data | https://newsapi.org/ |

---

## 2. Local Development Setup

### 2.1 Navigate to Project

```bash
cd "Async_API _aggregator"
```

### 2.2 Create Virtual Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2.3 Install Dependencies

```bash
# Install core dependencies
pip install fastapi uvicorn httpx cachetools pydantic pydantic-settings

# Install development dependencies
pip install pytest httpx

# Freeze dependencies
pip freeze > requirements.txt
```

---

## 3. API Keys Configuration

### 3.1 Environment Variables

Create a `.env` file (add to `.gitignore`):

```bash
# .env
OPENWEATHER_API_KEY=your_openweathermap_api_key
NEWS_API_KEY=your_newsapi_key
```

### 3.2 Setting API Keys

```bash
# Linux/macOS
export OPENWEATHER_API_KEY=your_key_here

# Windows (Command Prompt)
set OPENWEATHER_API_KEY=your_key_here

# Windows (PowerShell)
$env:OPENWEATHER_API_KEY="your_key_here"
```

### 3.3 Fallback Behavior

If API keys are not provided:
- **Weather**: Returns simulated data (no API call)
- **News**: Returns simulated data (no API call)
- System remains functional for testing

---

## 4. Running the Application

### 4.1 Start Development Server

```bash
# Navigate to project
cd "Async_API _aggregator"

# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --reload

# Or with custom settings
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4.2 Access Points

| Service | URL |
|---------|-----|
| **API Base URL** | http://127.0.0.1:8000 |
| **Interactive Docs** | http://127.0.0.1:8000/docs |
| **Alternative Docs** | http://127.0.0.1:8000/redoc |

### 4.3 Expected Output

```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 5. API Testing

### 5.1 Test Aggregation Endpoint

```bash
# Get aggregated data for a city
curl http://127.0.0.1:8000/aggregate/London

# Response:
# {
#   "city": "London",
#   "results": [
#     {"source": "weather", "status": "simulated", "data": {...}},
#     {"source": "news", "status": "ok", "data": [...]}
#   ],
#   "timing_ms": 823.5,
#   "sources_ok": 2
# }
```

### 5.2 Test with Cache

```bash
# First request (cache miss)
curl -v http://127.0.0.1:8000/aggregate/Tokyo
# Response header: X-Cache: MISS

# Second request (cache hit)
curl -v http://127.0.0.1:8000/aggregate/Tokyo
# Response header: X-Cache: HIT
```

### 5.3 Test Cache Bypass

```bash
# Force fresh data (bypass cache)
curl "http://127.0.0.1:8000/aggregate/Paris?no_cache=true"
# Response header: X-Cache: MISS
```

### 5.4 Test Cache Clearing

```bash
# Clear all cached data
curl -X DELETE http://127.0.0.1:8000/aggregate/cache

# Response: {"message": "Cache cleared"}
```

### 5.5 Test with HTTPie

```bash
# Install HTTPie
pip install httpie

# Test aggregation
http http://127.0.0.1:8000/aggregate/NewYork

# Test with no cache
http "http://127.0.0.1:8000/aggregate/Berlin?no_cache==true"
```

---

## 6. Docker Deployment

### 6.1 Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 6.2 Create .dockerignore

```
__pycache__/
*.pyc
.env
venv/
.git/
Dockerfile
```

### 6.3 Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
    volumes:
      - .:/app
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6.4 Build and Run

```bash
# Build Docker image
docker build -t async-aggregator .

# Run container
docker run -d -p 8000:8000 --name aggregator async-aggregator

# Or with Docker Compose
docker-compose up --build
```

---

## 7. Cloud Platform Deployment

### 7.1 Render

1. **Connect GitHub** - Link your repository
2. **Create Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**:
   ```
   OPENWEATHER_API_KEY=<your_key>
   ```

### 7.2 Railway

1. Create new project
2. Connect GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables

### 7.3 Google Cloud Run

```bash
# Build and deploy
gcloud run deploy async-aggregator \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY
```

---

## 8. Production Best Practices

### 8.1 Security Checklist

- [ ] **API Keys**: Store in environment variables, never commit
- [ ] **HTTPS**: Enable TLS/SSL in production
- [ ] **Rate Limiting**: Implement for external APIs
- [ ] **CORS**: Configure allowed origins
- [ ] **Logging**: Add structured logging

### 8.2 Cache Configuration

The current configuration in [`cache.py`](cache.py):

```python
cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes TTL
```

### 8.3 Scaling Considerations

| Aspect | Current | Production |
|--------|---------|------------|
| Cache | In-memory | Redis (recommended) |
| Workers | Single | Multiple |
| External APIs | Unlimited | Rate limited |

---

## 9. Performance Optimization

### 9.1 Understanding Concurrency Gains

```python
# Sequential (slower):
weather = await fetch_weather(city)     # ~500ms
news = await fetch_news(city)           # ~800ms
total = ~1300ms

# Concurrent (faster):
results = await asyncio.gather(
    fetch_weather(city),   # ~500ms
    fetch_news(city)       # ~800ms
)
total = ~800ms (max, not sum)
```

### 9.2 Running Multiple Workers

```bash
# Single worker (development)
uvicorn main:app --reload

# Multiple workers (production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 9.3 Cache Performance

| Metric | Target |
|--------|--------|
| Cache Hit | <50ms |
| Cache Miss | <1000ms |
| Hit Rate | >70% |

---

## 10. Troubleshooting

### 10.1 Common Issues

| Issue | Solution |
|-------|----------|
| Slow response | Check if APIs are being called or using fallback |
| Cache not working | Verify cachetools is installed |
| API errors | Check API keys are valid |
| Memory issues | TTLCache auto-evicts, but monitor usage |

### 10.2 Debug Logging

```python
# Add to your endpoint
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 10.3 Check Cache Status

```python
# Check cache directly
from cache import cache

print(f"Cache size: {len(cache)}")
print(f"Cache keys: {list(cache.keys())}")
```

### 10.4 Verify Async Behavior

```python
import asyncio
import time

async def test_concurrency():
    start = time.perf_counter()
    await asyncio.gather(
        asyncio.sleep(0.5),
        asyncio.sleep(0.8)
    )
    elapsed = time.perf_counter() - start
    print(f"Total time: {elapsed:.2f}s")  # Should be ~0.8s, not ~1.3s

asyncio.run(test_concurrency())
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| **Start Development** | `uvicorn main:app --reload` |
| **Test Aggregation** | `curl http://127.0.0.1:8000/aggregate/London` |
| **Clear Cache** | `curl -X DELETE http://127.0.0.1:8000/aggregate/cache` |
| **Docker Build** | `docker build -t async-aggregator .` |
| **Docker Run** | `docker run -p 8000:8000 async-aggregator` |
| **Multiple Workers** | `uvicorn main:app --workers 4` |

---

## Support & Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Asyncio Documentation**: https://docs.python.org/3/library/asyncio.html
- **httpx Documentation**: https://www.python-httpx.org/
- **cachetools Documentation**: https://cachetools.readthedocs.io/
- **OpenWeatherMap API**: https://openweathermap.org/api

---

**Document Version**: 1.1  
**Last Updated**: 2026-02-26
