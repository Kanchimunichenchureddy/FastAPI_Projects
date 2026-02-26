# Deployment Guide - "Background Tasks & Caching API"

This comprehensive guide provides instructions for setting up, developing, and deploying the Background Tasks & Caching API with Redis and MySQL.

> **Project**: Background Tasks & Caching API  
> **Framework**: FastAPI  
> **Database**: MySQL (Async via aiomysql)  
> **Cache**: Redis  
> **Python Version**: 3.12+  
> **Last Updated**: 2026-02-26

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Local Development Setup](#2-local-development-setup)
3. [Service Configuration](#3-service-configuration)
4. [Running the Application](#4-running-the-application)
5. [API Testing](#5-api-testing)
6. [Docker Deployment](#6-docker-deployment)
7. [Cloud Platform Deployment](#7-cloud-platform-deployment)
8. [Production Best Practices](#8-production-best-practices)
9. [Monitoring & Dashboard](#9-monitoring--dashboard)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.12 or higher | Runtime environment |
| **MySQL** | 8.0+ | Primary database |
| **Redis** | 6.0+ | Caching layer |
| **pip** | Latest | Package manager |

### 1.2 Installing Redis

#### macOS
```bash
# Using Homebrew
brew install redis
brew services start redis
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

#### Using Docker
```bash
# Run Redis container
docker run -d --name redis \
  -p 6379:6379 \
  redis:6-alpine
```

### 1.3 Installing MySQL

```bash
# Using Docker (recommended)
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=teja12345 \
  -e MYSQL_DATABASE=tasks_db \
  -p 3306:3306 \
  mysql:8.0
```

---

## 2. Local Development Setup

### 2.1 Navigate to Project

```bash
cd "Background _asks & Caching"
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
pip install fastapi uvicorn sqlalchemy aiomysql redis pydantic pydantic-settings

# Install development dependencies
pip install pytest httpx

# Freeze dependencies
pip freeze > requirements.txt
```

---

## 3. Service Configuration

### 3.1 Environment Variables

Create a `.env` file (add to `.gitignore`):

```bash
# .env
DB_USER=root
DB_PASSWORD=teja12345
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tasks_db
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 3.2 Redis Connection

The Redis connection is configured in [`utils.py`](utils.py:8):

```python
REDIS_URL = "redis://localhost:6379"
redis_client = redis.from_url(REDIS_URL, decode_responses=True)
```

### 3.3 MySQL Connection

The database connection is in [`database.py`](database.py:15):

```python
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

---

## 4. Running the Application

### 4.1 Start Development Server

```bash
# Navigate to project
cd "Background _asks & Caching"

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
| **Admin Dashboard** | http://127.0.0.1:8000/admin/dashboard |

### 4.3 Verify Services

```bash
# Check API status
curl http://127.0.0.1:8000/api/status

# Check Redis connection
redis-cli ping
# Should return: PONG

# Check MySQL connection
mysql -u root -p -e "SHOW DATABASES;"
```

---

## 5. API Testing

### 5.1 Test Background Tasks

```bash
# Create a background report task
curl -X POST http://127.0.0.1:8000/tasks/report \
  -H "Content-Type: application/json" \
  -d '{"report_type": "sales", "year": 2024}'

# Response: {"task_id": "uuid", "status": "pending"}

# Check task status (wait 10 seconds for completion)
curl http://127.0.0.1:8000/tasks/{task_id}
```

### 5.2 Test Caching

```bash
# First request (cache miss)
curl -v http://127.0.0.1:8000/expensive-query
# Should show X-Cache: MISS

# Second request (cache hit)
curl -v http://127.0.0.1:8000/expensive-query
# Should show X-Cache: HIT
```

### 5.3 Test Dashboard

```bash
# Get admin dashboard
curl http://127.0.0.1:8000/admin/dashboard

# Seed test orders
curl -X POST http://127.0.0.1:8000/orders/seed
```

---

## 6. Docker Deployment

### 6.1 Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

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

### 6.2 Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=teja12345
      - DB_NAME=tasks_db
      - REDIS_HOST=redis
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: teja12345
      MYSQL_DATABASE: tasks_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  mysql_data:
  redis_data:
```

### 6.3 Build and Run

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

---

## 7. Cloud Platform Deployment

### 7.1 Infrastructure Requirements

| Service | Requirement |
|---------|-------------|
| **MySQL** | AWS RDS, Google Cloud SQL, or managed MySQL |
| **Redis** | AWS ElastiCache, Redis Cloud, or managed Redis |

### 7.2 Render

1. **Create Services**:
   - Add MySQL database
   - Add Redis cache (using Render's Redis or external)

2. **Environment Variables**:
   ```
   DB_HOST=<mysql-host>
   DB_USER=<username>
   DB_PASSWORD=<password>
   DB_NAME=tasks_db
   REDIS_HOST=<redis-host>
   ```

3. **Deploy**: Connect GitHub repository

### 7.3 Railway

1. Create project with MySQL and Redis plugins
2. Configure environment variables
3. Deploy automatically

---

## 8. Production Best Practices

### 8.1 Performance Checklist

- [ ] Use Redis for caching (production)
- [ ] Configure appropriate TTL based on data volatility
- [ ] Use connection pooling for MySQL
- [ ] Monitor cache hit rate
- [ ] Use async/await throughout

### 8.2 Running Multiple Workers

```bash
# Single worker (development)
uvicorn main:app --reload

# Multiple workers (production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 8.3 Caching Strategy

| Data Type | Recommended TTL |
|-----------|-----------------|
| User profiles | 300-600 seconds |
| Statistics | 60-300 seconds |
| Expensive queries | 600-3600 seconds |
| Reference data | 3600+ seconds |

---

## 9. Monitoring & Dashboard

### 9.1 Admin Dashboard

The admin dashboard provides real-time statistics:

```bash
curl http://127.0.0.1:8000/admin/dashboard
```

Returns:
- Task statistics (total, pending, running, completed, failed)
- Cache statistics (hits, misses, hit rate)
- Recent tasks

### 9.2 Cache Headers

Every cached endpoint returns an `X-Cache` header:
- `HIT`: Response served from cache
- `MISS`: Response fetched from database
- `ERROR`: Redis connection error

---

## 10. Troubleshooting

### 10.1 Common Issues

| Issue | Solution |
|-------|----------|
| Redis connection refused | Ensure Redis is running on port 6379 |
| MySQL connection error | Verify credentials and database exists |
| Cache not working | Check Redis connectivity |
| Task not found | Check task_id is correct |

### 10.2 Debug Redis

```bash
# Check Redis connection
redis-cli ping

# View all keys
redis-cli KEYS "*"

# View cache stats
redis-cli INFO stats

# Clear all cache
redis-cli FLUSHALL
```

### 10.3 Debug Tasks

```python
# Check task store directly
from tasks import task_store

print(task_store)
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| **Start Development** | `uvicorn main:app --reload` |
| **Run Tests** | `pytest` |
| **Docker Compose** | `docker-compose up --build` |
| **Check Redis** | `redis-cli ping` |
| **View Cache Keys** | `redis-cli KEYS "*"` |
| **Clear Cache** | `redis-cli FLUSHALL` |
| **Production Run** | `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000` |

---

## Support & Resources

- **FastAPI Background Tasks**: https://fastapi.tiangolo.com/tutorial/background-tasks/
- **Redis Documentation**: https://redis.io/documentation
- **SQLAlchemy Async**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

---

**Document Version**: 1.1  
**Last Updated**: 2026-02-26
