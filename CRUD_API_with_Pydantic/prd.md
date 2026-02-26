# Product Requirements Document (PRD) - "CRUD API with Pydantic"

## 1. Project Overview

### Project Name
CRUD API with Pydantic & SQLAlchemy

### Project Type
RESTful API Service with Database Integration

### Project Description
A production-ready Task Management API demonstrating best practices in data validation using Pydantic v2 models and asynchronous database operations with SQLAlchemy. This project implements complete CRUD (Create, Read, Update, Delete) functionality with support for pagination, filtering, and data validation.

### Target Users
- **Primary**: Backend developers learning FastAPI with databases
- **Secondary**: Teams needing a quick task management backend template

---

## 2. Objectives

### Business Objectives
1. Provide complete CRUD operations for task management
2. Ensure strict data integrity through Pydantic validation
3. Support efficient data handling with pagination
4. Demonstrate async database patterns for scalability

### Learning Objectives
- Understand Pydantic v2 schema validation
- Learn SQLAlchemy async patterns with MySQL
- Implement pagination and filtering
- Handle database transactions (commit/rollback)

---

## 3. Core Features

### Feature 1: Create Task (`POST /tasks`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `POST /tasks` |
| **Description** | Create a new task with title, description, and priority |
| **User Story** | As a user, I want to create a task with a title, description, and priority level |
| **Request Body** | `TaskCreate` schema |
| **Path Parameters** | None |
| **Query Parameters** | None |
| **Request Fields** | |
| - `title` (string, required) | 1-100 characters, cannot be empty or whitespace |
| - `description` (string, optional) | Maximum 500 characters |
| - `priority` (enum, optional) | `low`, `medium` (default), `high` |
| **Response Format** | `JSON` |
| **Success Response (201)** | TaskResponse with id, created_at, updated_at |
| **Error Response (422)** | Validation Error with field-specific messages |
| **Use Case** | Adding new tasks to the system |

### Feature 2: List Tasks (`GET /tasks`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `GET /tasks` |
| **Description** | Retrieve all tasks with optional filtering and pagination |
| **User Story** | As a user, I want to see all my tasks with support for pagination and filtering |
| **Query Parameters** | |
| - `page` (int, optional) | Page number, default: 1, minimum: 1 |
| - `per_page` (int, optional) | Items per page, default: 10, range: 1-100 |
| - `completed` (bool, optional) | Filter by completion status |
| - `priority` (Priority, optional) | Filter by priority level |
| **Response Format** | `JSON` |
| **Success Response (200)** | TaskList containing tasks array, total count, page, per_page |
| **Response Fields** | |
| - `tasks` (array) | Array of TaskResponse objects |
| - `total` (int) | Total number of tasks matching filters |
| - `page` (int) | Current page number |
| - `per_page` (int) | Items per page |
| **Use Case** | Viewing task lists with pagination |

### Feature 3: Get Single Task (`GET /tasks/{task_id}`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `GET /tasks/{task_id}` |
| **Description** | Retrieve a specific task by its ID |
| **User Story** | As a user, I want to view the details of a specific task |
| **Path Parameters** | |
| - `task_id` (int, required) | The unique identifier of the task |
| **Response Format** | `JSON` |
| **Success Response (200)** | TaskResponse object |
| **Error Response (404)** | "Task not found" |
| **Use Case** | Viewing individual task details |

### Feature 4: Update Task (`PUT /tasks/{task_id}`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `PUT /tasks/{task_id}` |
| **Description** | Update an existing task (full update) |
| **User Story** | As a user, I want to update all fields of a task |
| **Path Parameters** | |
| - `task_id` (int, required) | The unique identifier of the task |
| **Request Body** | `TaskUpdate` schema (all fields optional) |
| **Request Fields** | |
| - `title` (string, optional) | 1-100 characters |
| - `description` (string, optional) | Maximum 500 characters |
| - `priority` (Priority, optional) | `low`, `medium`, `high` |
| - `completed` (bool, optional) | Completion status |
| **Response Format** | `JSON` |
| **Success Response (200)** | Updated TaskResponse object |
| **Error Response (404)** | "Task not found" |
| **Error Response (422)** | Validation Error |
| **Use Case** | Updating all fields of a task |

### Feature 5: Delete Task (`DELETE /tasks/{task_id}`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `DELETE /tasks/{task_id}` |
| **Description** | Delete a task permanently |
| **User Story** | As a user, I want to delete a task from the system |
| **Path Parameters** | |
| - `task_id` (int, required) | The unique identifier of the task |
| **Response Format** | None (Empty body) |
| **Success Response (204)** | No content |
| **Error Response (404)** | "Task not found" |
| **Use Case** | Removing tasks from the system |

### Feature 6: Root & Status Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check - "Hello teja! The CRUD API is running..." |
| `/api/status` | GET | API status with framework and database info |

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
| **Data Validation** | Pydantic | 2.x |
| **Database** | MySQL | 8.0+ |

### 4.2 Project Structure

```
CRUD_API_with_Pydantic/
├── main.py                  # FastAPI application entry point
├── database.py              # Database configuration and models
├── schemas.py               # Pydantic schemas (request/response)
├── routes/
│   └── tasks.py             # Task CRUD endpoints
├── tasks.db                 # SQLite fallback database file
├── teja/                    # Virtual environment
├── deployment_guide.md      # Deployment instructions
└── prd.md                   # This document
```

### 4.3 Database Schema

#### Task Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| title | String(100) | NOT NULL |
| description | String(500) | NULLABLE |
| priority | Enum | DEFAULT: medium |
| completed | Boolean | DEFAULT: False |
| created_at | DateTime | DEFAULT: UTC now |
| updated_at | DateTime | DEFAULT: UTC now, Auto-update |

### 4.4 API Endpoints Summary

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/` | Root health check | ✅ |
| GET | `/api/status` | API status | ✅ |
| GET | `/tasks` | List tasks (paginated) | ✅ |
| POST | `/tasks` | Create new task | ✅ |
| GET | `/tasks/{task_id}` | Get single task | ✅ |
| PUT | `/tasks/{task_id}` | Update task | ✅ |
| DELETE | `/tasks/{task_id}` | Delete task | ✅ |

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
- **Response Time**: <100ms for CRUD operations
- **Pagination**: Support up to 100 items per page
- **Async Operations**: All database operations must be async

### 5.2 Data Validation
- **Title**: 1-100 characters, cannot be empty or whitespace
- **Description**: Maximum 500 characters
- **Priority**: Must be one of: low, medium, high
- **Pydantic Validation**: All invalid data rejected before database

### 5.3 Error Handling
- **404 Not Found**: Task doesn't exist
- **422 Validation Error**: Invalid input data
- **500 Internal Server Error**: Database issues

### 5.4 Security Considerations
- **Input Sanitization**: All inputs validated via Pydantic
- **SQL Injection Prevention**: Using SQLAlchemy ORM
- **Database Credentials**: Via environment variables (production)

---

## 6. User Interactions and Flows

### Flow 1: Create a New Task
```
User → POST /tasks 
       Body: {"title": "Buy groceries", "priority": "high"}
       → Server validates input
       → Server inserts into MySQL
       → Server returns 201 with TaskResponse
```

### Flow 2: View Paginated Task List
```
User → GET /tasks?page=1&per_page=10&completed=false
       → Server queries MySQL with filters
       → Server returns paginated TaskList
```

### Flow 3: Update a Task
```
User → PUT /tasks/1
       Body: {"completed": true}
       → Server finds task in MySQL
       → Server updates fields
       → Server returns updated TaskResponse
```

### Flow 4: Delete a Task
```
User → DELETE /tasks/1
       → Server finds task in MySQL
       → Server deletes from database
       → Server returns 204 No Content
```

---

## 7. Success Metrics

### 7.1 Functional Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **All CRUD Endpoints Working** | 5/5 | Manual/automated testing |
| **Validation Accuracy** | 100% | Invalid data rejected with proper errors |
| **Database Integrity** | Zero data loss | Transaction handling verified |

### 7.2 Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Create Task Latency** | <100ms | Database insert time |
| **List Tasks Latency** | <150ms | Query + pagination |
| **Pagination Accuracy** | 100% | Total count matches |

### 7.3 Code Quality Metrics

| Metric | Target |
|--------|--------|
| **Type Hints** | All functions typed |
| **Docstrings** | All endpoints documented |
| **Error Handling** | All exceptions handled |

---

## 8. Future Enhancements

### Phase 2: User Management
- [ ] Add user registration and login
- [ ] Implement JWT authentication
- [ ] Add user-specific task ownership

### Phase 3: Advanced Features
- [ ] Task categories/labels
- [ ] Due dates and reminders
- [ ] Task comments/notes

### Phase 4: Performance & Scale
- [ ] Add database migrations (Alembic)
- [ ] Implement Redis caching
- [ ] Add rate limiting

### Phase 5: DevOps
- [ ] CI/CD pipeline
- [ ] Docker containerization
- [ ] Automated testing suite

---

## 9. Database Configuration

### 9.1 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DB_USER | root | MySQL username |
| DB_PASSWORD | teja12345 | MySQL password |
| DB_HOST | localhost | Database host |
| DB_PORT | 3306 | Database port |
| DB_NAME | tasks_db | Database name |

### 9.2 SQLite Fallback

The code includes commented SQLite configuration for local development:
```python
# DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"
```

---

## 10. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Database connection failure | Medium | High | Add connection pooling, retry logic |
| Validation bypass | Low | High | Pydantic strict mode |
| Pagination performance | Medium | Medium | Add database indices |
| Transaction failures | Low | Medium | Proper commit/rollback handling |

---

## 11. Glossary

| Term | Definition |
|------|------------|
| **CRUD** | Create, Read, Update, Delete - four basic database operations |
| **Pydantic** | Data validation library using Python type annotations |
| **SQLAlchemy** | SQL toolkit and ORM for Python |
| **AsyncIO** | Python library for writing concurrent code using async/await |
| **ORM** | Object-Relational Mapping - technique for converting between database and objects |
| **Pagination** | Dividing content into separate pages |
| **Schema** | Structure defining the shape of data |

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
