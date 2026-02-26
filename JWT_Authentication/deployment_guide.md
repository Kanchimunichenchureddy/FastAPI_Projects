# Deployment Guide - "JWT Authentication API"

## Local Development Setup

### 1. Prerequisites
- Python 3.12+
- MySQL Server

### 2. Environment Setup
```bash
# Navigate to project
cd "JWT_Authentication"

# Activate virtual environment
source venv/bin/activate
```

### 3. Core Dependencies
Install the required security and database packages:
```bash
pip install fastapi uvicorn sqlalchemy aiomysql python-jose[cryptography] passlib[bcrypt]
```

### 4. Configuration
> [!IMPORTANT]
> Change the `SECRET_KEY` in `auth.py` before deploying to any public-facing server.

### 5. Running the API
```bash
uvicorn main:app --reload
```
1. Visit `/docs`.
2. Use the `Authorize` button to test JWT flow.
3. Protected routes will return `401 Unauthorized` without a valid token.

## Production Best Practices
- **Secret Management**: Inject `SECRET_KEY`, `DB_USER`, and `DB_PASSWORD` via environment variables or a Secret Manager (e.g., AWS Secrets Manager).
- **HTTPS**: Always serve this API over HTTPS to protect tokens in transit.
- **SQL Tuning**: Ensure indices on `username` and `email` are maintained for fast authentication lookups.
- **Worker Configuration**:
  ```bash
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```
