# Deployment Guide - "My First API"

This guide provides instructions for setting up and deploying the FastAPI application.

## Local Development Setup

### 1. Prerequisites
- Python 3.12 or higher.
- `pip` (Python package manager).

### 2. Environment Setup
The project already contains a virtual environment folder `teja` in the `backend` directory.

```bash
# Navigate to the backend directory
cd backend

# Activate the virtual environment
source teja/bin/activate
```

### 3. Install Dependencies
Ensure you have the core dependencies installed:
```bash
pip install fastapi uvicorn
```

### 4. Running the Server Locally
Run the application using Uvicorn:
```bash
uvicorn main:app --reload
```
- Access the API at: `http://127.0.0.1:8000`
- Access documentation at: `http://127.0.0.1:8000/docs`

## Production Deployment Suggestions

### OPTION 1: Docker (Recommended)
Create a `Dockerfile` for easy containerization:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

### OPTION 2: Platform as a Service (PaaS)
- **Render / Railway**: Connect your GitHub repo, set the build command to `pip install -r requirements.txt` and start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- **AWS App Runner / Google Cloud Run**: Best for scalable, containerized deployments.

## Helpful Commands
- **Check Status**: `curl http://127.0.0.1:8000/api/status`
- **Freeze dependencies**: `pip freeze > requirements.txt`
