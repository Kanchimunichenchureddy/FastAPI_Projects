# Deployment Guide - "Async API Aggregator"

## Local Development Setup

### 1. Prerequisites
- Python 3.12+
- `pip`

### 2. Environment Setup
```bash
# Navigate to project
cd "Async_API _aggregator"

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn httpx cachetools
```

### 4. Running the Server
```bash
uvicorn main:app --reload
```
- API: `http://127.0.0.1:8000`
- Aggregate endpoint: `http://127.0.0.1:8000/aggregate/London`

## Production Considerations

### API Keys
> [!IMPORTANT]
> This project requires API keys for OpenWeather and NewsAPI. These should be provided via environment variables in production.

### Scaling
- Since the cache is in-memory (`TTLCache`), horizontal scaling (multiple instances) will lead to separate caches.
- For distributed systems, consider replacing `cachetools` with **Redis**.

### Deployment Command
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```
