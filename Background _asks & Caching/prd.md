# Product Requirements Document (PRD) - "Background Tasks & Caching API"

## 1. Project Overview

### Project Name
Background Tasks & Caching API

### Project Type
Enterprise-Grade API with Async Processing

### Project Description
A robust backend service designed to handle asynchronous processing and high-performance data retrieval. This project demonstrates background task processing using FastAPI's BackgroundTasks and Redis caching for optimized data access, along with MySQL for persistent storage.

### Target Users
- **Primary**: Developers learning async processing patterns
- **Secondary**: Teams building performance-critical applications

---

## 2. Objectives

### Business Objectives
1. Offload long-running processes to background tasks
2. Persist relational data using MySQL
3. Optimize read performance using Redis caching
4. Provide administrative endpoints for system monitoring

### Learning Objectives
- Understand FastAPI BackgroundTasks
- Implement Redis caching with TTL
- Build async database operations
- Create monitoring dashboards

---

## 3. Core Features

### Feature 1: Report Generation (`POST /tasks/report`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `POST /tasks/report` |
| **Description** | Trigger asynchronous report generation |
| **User Story** | As a user, I want to trigger a large report without waiting for it to finish |
| **Request Body** | Dictionary of parameters for the report |
| **Response Format** | `JSON` |
| **Success Response (202)** | `{"task_id": "uuid", "status": "pending"}` |
| **Mechanism** | Fast response immediately, processing continues in background |
| **Processing Time** | Simulated 10-second delay |
| **Background Task** | `generate_report()` function executes asynchronously |

### Feature 2: Task Status Tracking (`GET /tasks/{task_id}`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `GET /tasks/{task_id}` |
| **Description** | Check the status of a background task |
| **User Story** | As a user, I want to check if my report is ready |
| **Path Parameters** | |
| - `task_id` (string, required) | UUID of the task |
| **Response Format** | `JSON` |
| **Success Response (200)** | Task status object with all details |
| **Task States** | |
| - `pending` | Task created, waiting to start |
| - `running` | Task is currently processing |
| - `completed` | Task finished successfully |
| - `failed` | Task encountered an error |
| **Error Response (404)** | "Task not found" |

### Feature 3: Expensive Query with Caching (`GET /expensive-query`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `GET /expensive-query` |
| **Description** | Retrieve cached data to reduce database load |
| **User Story** | As a user, I want frequently accessed data to load instantly |
| **Caching** | Redis-backed cache with 600-second TTL |
| **Response Headers** | |
| - `X-Cache` | "HIT" (from cache) or "MISS" (fresh) |
| **Cache Key** | Based on request URL path and query parameters |
| **Cache TTL** | 600 seconds (10 minutes) |
| **Use Case** | Expensive database queries that don't change often |

### Feature 4: Order Seeding (`POST /orders/seed`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `POST /orders/seed` |
| **Description** | Seed test data for demonstration |
| **User Story** | As a developer, I want to populate the database with test data |
| **Response Format** | `JSON` |
| **Success Response (200)** | `{"message": "10 orders seeded"}` |
| **Action** | Creates 10 random orders with item names and amounts |

### Feature 5: Admin Dashboard (`GET /admin/dashboard`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `GET /admin/dashboard` |
| **Description** | System monitoring and statistics |
| **User Story** | As an admin, I want to see system performance metrics |
| **Response Format** | `JSON` |
| **Success Response (200)** | Dashboard with task and cache statistics |
| **Data Provided** | |
| - Task Statistics | Total, pending, running, completed, failed counts |
| - Cache Statistics | Hits, misses, hit rate, total keys |
| - Recent Tasks | Last 10 tasks with details |

### Feature 6: Root & Status Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check message |
| `/api/status` | GET | API status with features list, database, and cache info |

---

## 4. Technical Requirements

### 4.1 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Language** | Python | 3.12+ |
| **Web Framework** | FastAPI | Latest stable |
| **ASGI Server** | Uvicorn | Latest stable |
| **ORM** | SQLAlchemy | 2.0+ (async) |
| **Database Driver** | aiomysql | Latest |
| **Cache** | Redis | 6.0+ |
| **Redis Client** | redis-py (async) | Latest |
| **Database** | MySQL | 8.0+ |

### 4.2 Project Structure

```
Background _asks & Caching/
├── main.py                  # FastAPI application entry point
├── database.py              # Database configuration and Order model
├── tasks.py                 # Background task definitions
├── utils.py                 # Redis caching utilities and decorator
├── cache.py                # Cache router (now functioning as router)
├── routes/
│   └── admin.py            # Admin endpoints
├── venv/                   # Virtual environment
├── deployment_guide.md      # Deployment instructions
└── prd.md                  # This document
```

### 4.3 Database Schema

#### Orders Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| item_name | String(100) | NOT NULL |
| amount | Integer | NOT NULL |
| created_at | DateTime | DEFAULT: UTC now |

### 4.4 Task Store (In-Memory)

```python
task_store = {
    "task_id": {
        "id": "uuid",
        "type": "report",
        "status": "pending|running|completed|failed",
        "created_at": "ISO timestamp",
        "started_at": "ISO timestamp (optional)",
        "finished_at": "ISO timestamp (optional)",
        "result": {...} (optional),
        "error": "error message (optional)"
    }
}
```

### 4.5 Redis Cache Configuration

| Setting | Value |
|---------|-------|
| **URL** | redis://localhost:6379 |
| **TTL** | 600 seconds (10 minutes) |
| **Max Size** | 100 items (in-memory TTLCache) |
| **Key Format** | `cache:{path}:{query}` |

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

- **Background Tasks**: 0% blockage of main thread during processing
- **Cache Response Time**: <10ms for cache hits
- **Database Operations**: All async to prevent I/O bottlenecks

### 5.2 Caching Strategy

| Strategy | Implementation |
|----------|----------------|
| **TTL** | 600 seconds |
| **Cache Key** | Request URL + query parameters |
| **Invalidation** | Manual or TTL expiration |
| **Fallback** | Database query if cache miss |

### 5.3 Error Handling

| Status Code | Scenario |
|------------|----------|
| 202 | Task accepted (background processing) |
| 404 | Task not found |
| 500 | Task processing failed |

---

## 6. User Interactions and Flows

### Flow 1: Generate Report
```
User → POST /tasks/report
       Body: {"param1": "value1"}
       → Server creates task with PENDING status
       → Server returns 202 with task_id immediately
       → Background task starts processing (10 seconds)
       → User can check status with GET /tasks/{task_id}
```

### Flow 2: Check Task Status
```
User → GET /tasks/{task_id}
       → Server looks up task in task_store
       → Returns current task status and result/error
```

### Flow 3: Access Cached Data
```
User → GET /expensive-query
       → Check Redis for cached response
       → If HIT: Return cached data (X-Cache: HIT)
       → If MISS: Execute query, cache result, return (X-Cache: MISS)
```

### Flow 4: Admin Dashboard
```
User → GET /admin/dashboard
       → Gather task statistics from task_store
       → Gather Redis statistics (hits, misses, keys)
       → Return combined dashboard data
```

---

## 7. Success Metrics

### 7.1 Performance Metrics

| Metric | Target |
|--------|--------|
| Main thread unblocked | 100% during background processing |
| Cache hit response | <10ms |
| Cache miss response | <100ms |

### 7.2 Functional Metrics

| Metric | Target |
|--------|--------|
| Background tasks complete | All tasks eventually complete/fail |
| Task status accuracy | 100% accurate state tracking |
| Cache hit rate | Monitored via dashboard |

### 7.3 Monitoring Metrics

| Metric | Target |
|--------|--------|
| Dashboard accuracy | Real-time stats |
| Redis connection | Always connected |

---

## 8. Future Enhancements

### Phase 2: Enhanced Processing
- [ ] Use Celery for distributed task queue
- [ ] Add scheduled tasks (cron-like)
- [ ] Implement task chaining/pipelines

### Phase 3: Advanced Caching
- [ ] Redis Cluster for high availability
- [ ] Cache invalidation webhooks
- [ ] Distributed cache (Redis pub/sub)

### Phase 4: Monitoring & Logging
- [ ] Structured logging
- [ ] Error tracking (Sentry)
- [ ] Metrics export (Prometheus)

### Phase 5: Production Features
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment
- [ ] Auto-scaling

---

## 9. Infrastructure Configuration

### 9.1 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DB_USER | root | MySQL username |
| DB_PASSWORD | teja12345 | MySQL password |
| DB_HOST | localhost | Database host |
| DB_PORT | 3306 | Database port |
| DB_NAME | tasks_db | Database name |
| REDIS_HOST | localhost | Redis host |

### 9.2 Service Dependencies

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   FastAPI   │────▶│    MySQL    │     │    Redis    │
│   Server    │     │  Database   │     │    Cache    │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 10. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Redis connection failure | Medium | Medium | Graceful degradation to database-only |
| Task store memory issues | Low | Medium | Use Redis for task storage |
| Database connection pool | Medium | Medium | Configure pool size |
| Background task failure | Low | High | Proper error handling and logging |

---

## 11. Glossary

| Term | Definition |
|------|------------|
| **Background Task** | Processing that happens after HTTP response |
| **TTL** | Time To Live - how long data stays in cache |
| **Cache Hit** | Request served from cache |
| **Cache Miss** | Cache expired/not found, fetch from database |
| **Redis** | In-memory data store for caching |
| **AsyncIO** | Python library for concurrent operations |
| **Task Status** | State of background task (pending/running/completed/failed) |

---

## 12. Approval & Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Manager | [TBD] | [Date] | _______________ |
| Lead Developer | [TBD] | [Date] | _______________ |
| DevOps Engineer | [TBD] | [Date] | _______________ |

---

**Document Version**: 1.1  
**Last Updated**: 2026-02-26  
**Status**: Active
