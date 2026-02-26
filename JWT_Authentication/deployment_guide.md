# Deployment Guide - "JWT Authentication API"

This comprehensive guide provides instructions for setting up, developing, and deploying the JWT Authentication API with security best practices.

> **Project**: JWT Authentication API  
> **Framework**: FastAPI  
> **Database**: MySQL (Async via aiomysql)  
> **Authentication**: JWT (JSON Web Tokens)  
> **Python Version**: 3.12+  
> **Last Updated**: 2026-02-26

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Local Development Setup](#2-local-development-setup)
3. [Security Configuration](#3-security-configuration)
4. [Running the Application](#4-running-the-application)
5. [API Testing](#5-api-testing)
6. [Docker Deployment](#6-docker-deployment)
7. [Production Deployment](#7-production-deployment)
8. [Production Best Practices](#8-production-best-practices)
9. [CI/CD Pipeline](#9-cicd-pipeline)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.12 or higher | Runtime environment |
| **MySQL** | 8.0+ | User and task database |
| **pip** | Latest | Package manager |
| **git** | Latest | Version control |

### 1.2 Installing MySQL

#### macOS
```bash
# Using Homebrew
brew install mysql
brew services start mysql
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

#### Using Docker
```bash
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
cd JWT_Authentication
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
pip install fastapi uvicorn sqlalchemy aiomysql python-jose[cryptography] passlib[bcrypt] pydantic pydantic-settings

# Install development dependencies
pip install pytest httpx

# Freeze dependencies
pip freeze > requirements.txt
```

---

## 3. Security Configuration

### 3.1 Generate Secure Secret Key

```bash
# Generate a secure random secret key
python -c "from secrets import token_hex; print(token_hex(32))"

# Output: a1b2c3d4e5f6... (save this)
```

### 3.2 Environment Variables

Create a `.env` file (add to `.gitignore`):

```bash
# .env
SECRET_KEY=your-generated-secret-key-here
DB_USER=root
DB_PASSWORD=teja12345
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tasks_db
```

### 3.3 Update auth.py for Production

In [`auth.py`](auth.py:6), update the secret key configuration:

```python
# For production, use environment variable
import os
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
```

---

## 4. Running the Application

### 4.1 Start Development Server

```bash
# Navigate to project
cd JWT_Authentication

# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --reload

# Or with custom port
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4.2 Access Points

| Service | URL |
|---------|-----|
| **API Base URL** | http://127.0.0.1:8000 |
| **Interactive Docs** | http://127.0.0.1:8000/docs |
| **Alternative Docs** | http://127.0.0.1:8000/redoc |

### 4.3 Authorize in Swagger UI

1. Visit `/docs`
2. Click the **Authorize** button
3. Enter your credentials
4. All protected endpoints will now work

---

## 5. API Testing

### 5.1 Test Authentication Flow

```bash
# Register a new user
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'

# Login (form data)
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepassword123"

# Get current user profile
curl -X GET http://127.0.0.1:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5.2 Test Protected Endpoints

```bash
# Create a task (requires authentication)
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Task", "priority": "high"}'

# List tasks (requires authentication)
curl -X GET "http://127.0.0.1:8000/tasks?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5.3 Test with HTTPie

```bash
# Install HTTPie
pip install httpie

# Register
http POST http://127.0.0.1:8000/auth/register \
  username=johndoe \
  email=john@example.com \
  password=securepassword123

# Login (this saves the token)
http --form POST http://127.0.0.1:8000/auth/login \
  username=john@example.com \
  password=securepassword123

# Get profile
http GET http://127.0.0.1:8000/auth/me \
  Authorization:"Bearer YOUR_TOKEN"

# Create task
http POST http://127.0.0.1:8000/tasks \
  Authorization:"Bearer YOUR_TOKEN" \
  title="My Task" \
  priority=high
```

---

## 6. Docker Deployment

### 6.1 Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    libffi-dev \
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
      - SECRET_KEY=your-production-secret-key
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=teja12345
      - DB_NAME=tasks_db
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: teja12345
      MYSQL_DATABASE: tasks_db
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### 6.4 Build and Run

```bash
docker-compose up --build
```

---

## 7. Production Deployment

### 7.1 Cloud Platforms

#### Render
1. Connect GitHub repository
2. Create Web Service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables:
   ```
   SECRET_KEY=<your-secure-key>
   DB_HOST=<mysql-host>
   DB_USER=<username>
   DB_PASSWORD=<password>
   DB_NAME=tasks_db
   ```

#### Railway
1. Create new project
2. Add MySQL database
3. Configure environment variables
4. Deploy

### 7.2 AWS EC2

```bash
# SSH to EC2
ssh -i your-key.pem ec2-user@your-ip

# Install Python and dependencies
sudo yum install python3.12 python3.12-pip
git clone your-repo
cd JWT_Authentication
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with systemd
sudo vim /etc/systemd/system/jwt-api.service
```

Systemd service:
```ini
[Unit]
Description=JWT Authentication API
After=network.target mysql.service

[Service]
Type=notify
User=ec2-user
WorkingDirectory=/home/ec2-user/JWT_Authentication
Environment="PATH=/home/ec2-user/JWT_Authentication/venv/bin"
Environment="SECRET_KEY=your-production-secret"
ExecStart=/home/ec2-user/JWT_Authentication/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 8. Production Best Practices

### 8.1 Security Checklist

- [ ] **SECRET_KEY**: Generate and use a strong random key
- [ ] **HTTPS**: Always use TLS/SSL
- [ ] **Environment Variables**: Never commit secrets to git
- [ ] **Password Hashing**: Already using bcrypt (good!)
- [ ] **Token Expiry**: Access tokens expire in 30 minutes (good!)
- [ ] **Database**: Use separate user with minimal permissions
- [ ] **CORS**: Configure allowed origins
- [ ] **Rate Limiting**: Add to prevent brute force attacks

### 8.2 Database Security

```sql
-- Create application user with limited permissions
CREATE USER 'api_user'@'%' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON tasks_db.* TO 'api_user'@'%';
FLUSH PRIVILEGES;
```

### 8.3 Running in Production

```bash
# Single worker
uvicorn main:app --host 0.0.0.0 --port 8000

# Multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn (recommended)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 8.4 Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # For HTTPS
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

---

## 9. CI/CD Pipeline

### 9.1 GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy JWT Authentication API

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
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          
      - name: Run tests
        run: |
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
| Invalid credentials error | Check email and password match |
| Token expired | Use refresh token to get new access token |
| 401 Unauthorized | Include valid Bearer token in header |
| Database connection | Verify MySQL is running and credentials are correct |
| bcrypt issues | Ensure build tools are installed for Docker |

### 10.2 Debug Token Issues

```python
# Test token decoding
from auth import decode_token, SECRET_KEY, ALGORITHM
from jose import jwt

# Decode manually
token = "your-token-here"
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print(payload)
```

### 10.3 Check Database Users

```python
# List users in database
from database import async_session
from sqlalchemy import select, User

async def list_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for u in users:
            print(f"{u.id}: {u.username} ({u.email})")
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| **Start Development** | `uvicorn main:app --reload` |
| **Generate Secret Key** | `python -c "from secrets import token_hex; print(token_hex(32))"` |
| **Test Registration** | `http POST /auth/register username=jdoe email=j@example.com password=pass` |
| **Test Login** | `http --form POST /auth/login username=j@example.com password=pass` |
| **Docker Build** | `docker build -t jwt-api .` |
| **Production Run** | `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000` |

---

## Support & Resources

- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/
- **JWT Documentation**: https://pyjwt.readthedocs.io/
- **Passlib**: https://passlib.readthedocs.io/
- **OAuth 2.0**: https://oauth.net/2/

---

**Document Version**: 1.1  
**Last Updated**: 2026-02-26
