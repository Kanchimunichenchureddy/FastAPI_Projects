# FastAPI Projects

A comprehensive collection of FastAPI projects demonstrating various backend development patterns, from basic API concepts to advanced features like authentication, background tasks, caching, and API aggregation.

> **Framework**: FastAPI  
> **Language**: Python 3.12+  
> **Database**: MySQL / SQLite  
> **Cache**: Redis  

---

## Table of Contents

- [Projects Overview](#projects-overview)
- [Getting Started](#getting-started)
- [Project Details](#project-details)
  - [Flask_Quick_start](#1-flask_quick_start)
  - [CRUD_API_with_Pydantic](#2-crud_api_with_pydantic)
  - [JWT_Authentication](#3-jwt_authentication)
  - [Background Tasks \& Caching](#4-background-tasks--caching)
  - [Async_API Aggregator](#5-async_api-aggregator)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Projects Overview

| Project | Description | Difficulty | Key Features |
|---------|-------------|------------|--------------|
| **Flask_Quick_start** | Basic FastAPI introduction | ⭐ Beginner | Routes, Path Parameters, Query Parameters, Auto Docs |
| **CRUD_API_with_Pydantic** | Full CRUD operations | ⭐⭐ Intermediate | SQLAlchemy Async, Pydantic Validation, MySQL |
| **JWT_Authentication** | Secure API with auth | ⭐⭐⭐ Advanced | JWT Tokens, bcrypt, OAuth2, Protected Routes |
| **Background Tasks & Caching** | Performance optimization | ⭐⭐⭐ Advanced | Redis Cache, Background Tasks, Admin Dashboard |
| **Async_API Aggregator** | API integration | ⭐⭐⭐ Advanced | asyncio, Concurrent Requests, TTL Cache |

---

## Getting Started

### Prerequisites

```bash
# Required software
- Python 3.12 or higher
- MySQL 8.0+ (for some projects)
- Redis 6.0+ (for caching projects)
- Git
```

### Installation

```bash
# Clone the repository
git clone https://github.com/Kanchimunichenchureddy/FastAPI_Projects.git
cd FastAPI_Projects

# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Project Details

---

### 1. Flask_Quick_start

A beginner-friendly introduction to FastAPI with basic endpoints.

**Location**: `Flask_Quick_start/`

**Features**:
- Root endpoint (`/`)
- Personalized greeting (`/greet/{name}`)
- Status monitoring (`/api/status`)
- Automatic API documentation at `/docs`

**Run**:
```bash
cd Flask_Quick_start/backend
source teja/bin/activate
uvicorn main:app --reload
```

**Access**:
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

**Documentation**:
- [PRD](Flask_Quick_start/prd.md)
- [Deployment Guide](Flask_Quick_start/deployment_guide.md)

---

### 2. CRUD_API_with_Pydantic

Complete CRUD API with data validation using Pydantic and async database operations.

**Location**: `CRUD_API_with_Pydantic/`

**Features**:
- Create, Read, Update, Delete operations
- Pydantic v2 schema validation
- SQLAlchemy async with MySQL
- Pagination and filtering
- Database migrations ready

**Endpoints**:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List tasks (paginated) |
| POST | `/tasks` | Create new task |
| GET | `/tasks/{id}` | Get single task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

**Run**:
```bash
cd CRUD_API_with_Pydantic
source teja/bin/activate
uvicorn main:app --reload
```

**Environment Variables**:
```bash
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tasks_db
```

**Documentation**:
- [PRD](CRUD_API_with_Pydantic/prd.md)
- [Deployment Guide](CRUD_API_with_Pydantic/deployment_guide.md)

---

### 3. JWT_Authentication

Secure API with JSON Web Token authentication and user management.

**Location**: `JWT_Authentication/`

**Features**:
- User registration (`/auth/register`)
- User login with JWT (`/auth/login`)
- Token refresh mechanism
- Protected routes
- Password hashing with bcrypt
- User-specific data isolation

**Endpoints**:
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get tokens |
| GET | `/auth/me` | Get current user profile |
| GET | `/tasks` | List user's tasks (protected) |
| POST | `/tasks` | Create task (protected) |

**Run**:
```bash
cd JWT_Authentication
source venv/bin/activate
uvicorn main:app --reload
```

**Security**:
- Access tokens expire in 30 minutes
- Refresh tokens expire in 7 days
- Passwords hashed with bcrypt

**Documentation**:
- [PRD](JWT_Authentication/prd.md)
- [Deployment Guide](JWT_Authentication/deployment_guide.md)

---

### 4. Background Tasks & Caching

Enterprise-grade API with background task processing and Redis caching.

**Location**: `Background _asks & Caching/`

**Features**:
- Background task processing with FastAPI BackgroundTasks
- Redis caching with TTL (600 seconds)
- Admin dashboard with statistics
- Concurrent data processing
- Order management with MySQL

**Endpoints**:
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/report` | Create background report task |
| GET | `/tasks/{task_id}` | Check task status |
| GET | `/expensive-query` | Cached database query |
| POST | `/orders/seed` | Seed test data |
| GET | `/admin/dashboard` | System monitoring |

**Run**:
```bash
cd "Background _asks & Caching"
source venv/bin/activate

# Start Redis first
redis-server

# Start API
uvicorn main:app --reload
```

**Services Required**:
- MySQL (port 3306)
- Redis (port 6379)

**Documentation**:
- [PRD](Background _asks & Caching/prd.md)
- [Deployment Guide](Background _asks & Caching/deployment_guide.md)

---

### 5. Async_API Aggregator

High-performance API that aggregates data from multiple sources concurrently.

**Location**: `Async_API _aggregator/`

**Features**:
- Concurrent API fetching using asyncio.gather
- TTL caching (5 minutes)
- Weather data integration (OpenWeatherMap)
- News data aggregation
- Cache management endpoints
- Performance timing metrics

**Endpoints**:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/aggregate/{city}` | Get weather + news for city |
| DELETE | `/aggregate/cache` | Clear all cached data |

**Query Parameters**:
- `no_cache` (bool): Force fresh data instead of cache

**Run**:
```bash
cd "Async_API _aggregator"
source venv/bin/activate
uvicorn main:app --reload
```

**API Keys** (Optional):
```bash
OPENWEATHER_API_KEY=your_key_here
```

**Performance**:
- Concurrent fetching: ~800ms (vs ~1300ms sequential)
- Cache hits: <50ms response time

**Documentation**:
- [PRD](Async_API _aggregator/prd.md)
- [Deployment Guide](Async_API _aggregator/deployment_guide.md)

---

## Technology Stack

### Core Technologies

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **Uvicorn** | ASGI server |
| **Python 3.12+** | Runtime |
| **Pydantic** | Data validation |

### Database & Cache

| Technology | Purpose |
|------------|---------|
| **SQLAlchemy** | ORM |
| **MySQL** | Primary database |
| **Redis** | Caching layer |
| **aiomysql** | Async MySQL driver |

### Security

| Technology | Purpose |
|------------|---------|
| **python-jose** | JWT tokens |
| **passlib** | Password hashing |
| **bcrypt** | Encryption |

### Additional

| Technology | Purpose |
|------------|---------|
| **httpx** | Async HTTP client |
| **cachetools** | In-memory cache |
| **Docker** | Containerization |

---

## Quick Start

### Running All Projects

```bash
# Project 1: Basic API
cd Flask_Quick_start/backend
uvicorn main:app --reload --port 8001

# Project 2: CRUD API (new terminal)
cd CRUD_API_with_Pydantic
uvicorn main:app --reload --port 8002

# Project 3: Auth API (new terminal)
cd JWT_Authentication
uvicorn main:app --reload --port 8003

# Project 4: Background Tasks (needs Redis + MySQL)
cd "Background _asks & Caching"
uvicorn main:app --reload --port 8004

# Project 5: API Aggregator
cd "Async_API _aggregator"
uvicorn main:app --reload --port 8005
```

### Using Docker

```bash
# Build and run any project
cd <project-directory>
docker-compose up --build
```

---

## Deployment

### Recommended Platforms

| Platform | Best For |
|----------|----------|
| **Render** | Easy deployment, free tier available |
| **Railway** | Modern, developer-friendly |
| **AWS** | Enterprise, scalable |
| **Google Cloud Run** | Serverless containers |
| **Azure** | Microsoft ecosystem |

### Environment Variables for Production

```bash
# Common variables
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Database
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password

# Redis (if needed)
REDIS_HOST=your-redis-host
```

### Docker Production

```bash
# Build image
docker build -t your-app:latest .

# Run container
docker run -d -p 8000:8000 \
  -e DB_HOST=your-db-host \
  -e SECRET_KEY=your-secret \
  your-app:latest
```

---

## Project Structure

```
FastAPI_Projects/
├── Flask_Quick_start/           # Basic API
│   ├── backend/
│   │   ├── main.py
│   │   └── teja/              # Virtual environment
│   ├── prd.md
│   └── deployment_guide.md
│
├── CRUD_API_with_Pydantic/     # CRUD operations
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes/
│   ├── prd.md
│   └── deployment_guide.md
│
├── JWT_Authentication/         # Auth system
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── routes/
│   ├── prd.md
│   └── deployment_guide.md
│
├── Background _asks & Caching/ # Performance
│   ├── main.py
│   ├── database.py
│   ├── tasks.py
│   ├── utils.py
│   ├── routes/
│   ├── prd.md
│   └── deployment_guide.md
│
├── Async_API _aggregator/     # API integration
│   ├── main.py
│   ├── clients.py
│   ├── cache.py
│   ├── routers/
│   ├── prd.md
│   └── deployment_guide.md
│
└── README.md
```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Author**: Teja Kanchi  
**GitHub**: [Kanchimunichenchureddy](https://github.com/Kanchimunichenchureddy)  
**Last Updated**: 2026-02-26
