# Deployment Guide - "Background Tasks & Caching"

## Local Development Setup

### 1. Prerequisites
- Python 3.12+
- MySQL Server (running on `localhost:3306`)
- Redis Server (running on `localhost:6379`)

### 2. Environment Variables
Set the following environment variables if your local configuration differs from the defaults:
```bash
export DB_USER="root"
export DB_PASSWORD="your_password"
export DB_NAME="tasks_db"
export REDIS_HOST="localhost"
```

### 3. Setup and Run
```bash
# Navigate to project
cd "Background _asks & Caching"

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy aiomysql redis
```

### 4. Database Initialization
The application automatically creates the necessary tables on startup via `init_db()`.

### 5. Running the API
```bash
uvicorn main:app --reload
```

## Production Deployment Suggestions

### Infrastructure
- **Managed Database**: Use AWS RDS or Google Cloud SQL (MySQL).
- **Managed Cache**: Use AWS ElastiCache or Redis Labs.

### Containerization (Docker Compose)
Highly recommended to manage the API, MySQL, and Redis services together:
```yaml
services:
  api:
    build: .
    environment:
      - DB_HOST=db
      - REDIS_HOST=redis
  db:
    image: mysql:8.0
  redis:
    image: redis:6-alpine
```

### Process Management
Run multiple workers in production to handle heavy load:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```
