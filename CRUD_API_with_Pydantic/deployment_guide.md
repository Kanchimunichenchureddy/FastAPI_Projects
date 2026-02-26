# Deployment Guide - "CRUD API with Pydantic"

This comprehensive guide provides instructions for setting up, developing, and deploying the CRUD API with Pydantic and SQLAlchemy.

> **Project**: CRUD API with Pydantic & SQLAlchemy  
> **Framework**: FastAPI  
> **Database**: MySQL (Async via aiomysql)  
> **Python Version**: 3.12+  
> **Last Updated**: 2026-02-26

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Local Development Setup](#2-local-development-setup)
3. [Database Configuration](#3-database-configuration)
4. [Running the Application](#4-running-the-application)
5. [API Testing](#5-api-testing)
6. [Docker Deployment](#6-docker-deployment)
7. [Cloud Platform Deployment](#7-cloud-platform-deployment)
8. [Production Best Practices](#8-production-best-practices)
9. [Database Migrations](#9-database-migrations)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.12 or higher | Runtime environment |
| **MySQL** | 8.0+ | Primary database |
| **pip** | Latest | Package manager |
| **git** | Latest | Version control |

### 1.2 Installing MySQL

#### macOS
```bash
# Using Homebrew
brew install mysql
brew services start mysql

# Or use Docker
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=teja12345 -p 3306:3306 mysql:8.0
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### Windows
- Download MySQL Installer from [mysql.com](https://www.mysql.com/downloads/)
- Or use [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 1.3 Create Database

```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE tasks_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verify
SHOW DATABASES;
```

---

## 2. Local Development Setup

### 2.1 Clone/Navigate to Project

```bash
# Navigate to project directory
cd CRUD_API_with_Pydantic
```

### 2.2 Create Virtual Environment

#### Option A: Using Existing Virtual Environment

```bash
# Activate the pre-configured virtual environment
source teja/bin/activate

# Verify Python version
python --version
```

#### Option B: Creating New Virtual Environment

```bash
# Create new virtual environment
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
pip install fastapi uvicorn sqlalchemy aiomysql pydantic pydantic-settings

# Install development dependencies
pip install pytest pytest-asyncio httpx

# Freeze dependencies
pip freeze > requirements.txt
```

---

## 3. Database Configuration

### 3.1 Environment Variables

Create a `.env` file (add to `.gitignore`):

```bash
# .env
DB_USER=root
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tasks_db

# Optional: Use SQLite for local development
# DB_URL=sqlite+aiosqlite:///./tasks.db
```

### 3.2 Database Connection

The application uses MySQL by default. The connection is configured in [`database.py`](database.py:14):

```python
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

### 3.3 SQLite Fallback (Development)

For local development without MySQL, uncomment the SQLite line in [`database.py`](database.py:10):

```python
# Use SQLite for local development
DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"
```

---

## 4. Running the Application

### 4.1 Development Mode

```bash
# Navigate to project directory
cd CRUD_API_with_Pydantic

# Activate virtual environment
source teja/bin/activate

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
| **OpenAPI Schema** | http://127.0.0.1:8000/openapi.json |

### 4.3 Expected Output

```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 5. API Testing

### 5.1 Test Endpoints with curl

```bash
# Root endpoint
curl http://127.0.0.1:8000/

# API status
curl http://127.0.0.1:8000/api/status

# Create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "priority": "high"}'

# List tasks
curl "http://127.0.0.1:8000/tasks?page=1&per_page=10"

# Get single task
curl http://127.0.0.1:8000/tasks/1

# Update task
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete task
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

### 5.2 Test with HTTPie (Recommended)

```bash
# Install HTTPie
pip install httpie

# Test endpoints
http http://127.0.0.1:8000/
http POST http://127.0.0.1:8000/tasks title="Buy groceries" priority=high
http "http://127.0.0.1:8000/tasks?page=1&per_page=5"
```

---

## 6. Docker Deployment

### 6.1 Create Dockerfile

Create a `Dockerfile` in the project root:

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

### 6.2 Create .dockerignore

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.env
.venv/
venv/
teja/
*.db
.git/
.gitignore
Dockerfile
docker-compose.yml
```

### 6.3 Docker Compose (Recommended)

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
    depends_on:
      - db
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

volumes:
  mysql_data:
```

### 6.4 Build and Run

```bash
# Build and start services
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

### 7.1 Render

1. **Connect GitHub** - Link your repository to Render
2. **Create Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**:
   ```
   DB_HOST=<your-mysql-host>
   DB_USER=<username>
   DB_PASSWORD=<password>
   DB_NAME=tasks_db
   ```

### 7.2 Railway

1. **Create Project** - Connect GitHub repository
2. **Add MySQL** - Provision MySQL service
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Deploy** - Automatic deployment on push

### 7.3 AWS (EC2/RDS)

```bash
# Launch RDS instance (MySQL)
# Configure security group for port 3306

# SSH to EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# Clone and deploy
git clone your-repo
cd CRUD_API_with_Pydantic
source venv/bin/activate
pip install -r requirements.txt

# Run with systemd
sudo vim /etc/systemd/system/crud-api.service
```

Create systemd service:
```ini
[Unit]
Description=CRUD API Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/CRUD_API_with_Pydantic
ExecStart=/home/ec2-user/CRUD_API_with_Pydantic/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 8. Production Best Practices

### 8.1 Security Checklist

- [ ] **Never commit credentials** to version control
- [ ] Use environment variables or secret managers
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Run with non-root user in containers
- [ ] Keep dependencies updated
- [ ] Implement rate limiting

### 8.2 Performance Checklist

- [ ] Use connection pooling
- [ ] Add database indices on frequently queried columns
- [ ] Implement caching for read-heavy operations
- [ ] Use async/await throughout
- [ ] Configure appropriate worker count

### 8.3 Production Uvicorn Command

```bash
# Single worker (for testing)
uvicorn main:app --host 0.0.0.0 --port 8000

# Multiple workers (production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn (recommended)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

---

## 9. Database Migrations

### 9.1 Why Use Migrations?

- Track schema changes over time
- Rollback capability
- Team collaboration
- CI/CD integration

### 9.2 Setting Up Alembic

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init migrations

# Configure alembic.ini with your database URL
sqlalchemy.url = mysql+aiomysql://root:password@localhost/tasks_db

# Create migration
alembic revision --autogenerate -m "Add tasks table"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 10. Troubleshooting

### 10.1 Common Issues

| Issue | Solution |
|-------|----------|
| **MySQL connection refused** | Ensure MySQL is running and credentials are correct |
| **Database doesn't exist** | Create the database: `CREATE DATABASE tasks_db;` |
| **ModuleNotFoundError** | Activate virtual environment and reinstall |
| **Port in use** | Kill process: `lsof -ti:8000 \| xargs kill` |
| **Permission denied** | Check file permissions |

### 10.2 Check Database Connection

```python
# Test database connection
import asyncio
from database import engine

async def test_db():
    async with engine.begin() as conn:
        print("Database connected successfully!")

asyncio.run(test_db())
```

### 10.3 Debug Mode

```bash
# Enable debug logging
uvicorn main:app --log-level debug --reload

# Check database echo
# In database.py, set: engine = create_async_engine(DATABASE_URL, echo=True)
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| **Start Development** | `uvicorn main:app --reload` |
| **Run Tests** | `pytest` |
| **Create Migration** | `alembic revision --autogenerate -m "message"` |
| **Apply Migrations** | `alembic upgrade head` |
| **Docker Build** | `docker build -t crud-api .` |
| **Docker Run** | `docker run -p 8000:8000 crud-api` |
| **Docker Compose** | `docker-compose up --build` |

---

## Support & Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **Alembic Documentation**: https://alembic.sqlalchemy.org/

---

**Document Version**: 1.1  
**Last Updated**: 2026-02-26
