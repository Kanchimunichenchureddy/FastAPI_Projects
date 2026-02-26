# Deployment Guide - "CRUD API with Pydantic"

## Local Development Setup

### 1. Prerequisites
- Python 3.12+
- MySQL Server

### 2. Environment Configuration
The API is configured to connect to MySQL. Set your credentials:
```bash
export DB_USER="root"
export DB_PASSWORD="your_password"
export DB_NAME="tasks_db"
```

### 3. Setup and Run
```bash
# Navigate to project
cd "CRUD_API_with_Pydantic"

# Activate virtual environment
source teja/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy aiomysql pydantic
```

### 4. Running the API
```bash
uvicorn main:app --reload
```
- API root: `http://127.0.0.1:8000`
- Documentation: `http://127.0.0.1:8000/docs`

## Database Management
- The application will attempt to create the `tasks` table on startup.
- If you prefer SQLite, modify `database.py` to use the `sqlite+aiosqlite` URL.

## Production Best Practices
- **Security**: Never commit `DB_PASSWORD` to version control. Use a secret manager.
- **Migrations**: For future schema changes, consider using **Alembic**.
- **Workers**: Use Gunicorn with Uvicorn workers for production stability:
  ```bash
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
  ```
