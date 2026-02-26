# Product Requirements Document (PRD) - "JWT Authentication API"

## 1. Project Overview

### Project Name
JWT Authentication API

### Project Type
Secure RESTful API with Authentication

### Project Description
A secure, multi-user task management API featuring robust authentication via JSON Web Tokens (JWT) with persistent user profiles. This project implements industry-standard security practices including password hashing, token-based authentication, and user-specific data ownership.

### Target Users
- **Primary**: Developers learning JWT authentication with FastAPI
- **Secondary**: Teams needing a secure user authentication template

---

## 2. Objectives

### Business Objectives
1. Secure all sensitive endpoints behind authentication
2. Implement user-specific data ownership (users only see their own tasks)
3. Provide industry-standard password security (bcrypt hashing)
4. Support scalable authentication via stateless JWT tokens

### Learning Objectives
- Understand JWT token generation and validation
- Implement OAuth2 password flow
- Learn bcrypt password hashing
- Implement protected routes with dependency injection

---

## 3. Core Features

### Feature 1: User Registration (`POST /auth/register`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `POST /auth/register` |
| **Description** | Register a new user account |
| **User Story** | As a new user, I want to create an account with my email and username |
| **Request Body** | `UserCreate` schema |
| **Request Fields** | |
| - `username` (string, required) | Unique username (max 50 chars) |
| - `email` (EmailStr, required) | Valid email address |
| - `password` (string, required) | User password |
| **Response Format** | `JSON` |
| **Success Response (201)** | UserResponse without password_hash |
| **Error Response (409)** | "Email already registered" or "Username already taken" |
| **Error Response (422)** | Validation error |
| **Security** | Password is hashed with bcrypt before storage |

### Feature 2: User Login (`POST /auth/login`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `POST /auth/login` |
| **Description** | Authenticate user and receive JWT tokens |
| **User Story** | As a registered user, I want to log in and receive access and refresh tokens |
| **Authentication** | OAuth2 Password Flow (form data) |
| **Request Fields** | |
| - `username` (string, required) | Email address (used as username) |
| - `password` (string, required) | User password |
| **Response Format** | `JSON` |
| **Success Response (200)** | TokenResponse with access_token, refresh_token, token_type |
| **Error Response (401)** | "Invalid credentials" |
| **Token Details** | |
| - Access Token | Expires in 30 minutes |
| - Refresh Token | Expires in 7 days |

### Feature 3: Get Current User Profile (`GET /auth/me`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `GET /auth/me` |
| **Description** | Retrieve the currently authenticated user's profile |
| **User Story** | As a logged-in user, I want to see my registered details |
| **Authentication** | Bearer token (required) |
| **Response Format** | `JSON` |
| **Success Response (200)** | UserResponse (id, username, email, created_at) |
| **Error Response (401)** | "Could not validate credentials" |

### Feature 4: Create Task (`POST /tasks`) - Protected

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `POST /tasks` |
| **Description** | Create a task owned by the current user |
| **User Story** | As a logged-in user, I want to create a personal task |
| **Authentication** | Bearer token (required) |
| **Authorization** | User can only create tasks for themselves |
| **Request Body** | `TaskCreate` schema |
| **Request Fields** | |
| - `title` (string, required) | 1-100 characters |
| - `description` (string, optional) | Max 500 characters |
| - `priority` (Priority, optional) | low, medium, high |
| **Response Format** | `JSON` |
| **Success Response (201)** | TaskResponse with owner_id set to current user |
| **Auto-Assignment** | owner_id automatically set from JWT token |

### Feature 5: List Tasks (`GET /tasks`) - Protected

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `GET /tasks` |
| **Description** | List tasks owned by the current user |
| **User Story** | As a logged-in user, I want to see only my personal tasks |
| **Authentication** | Bearer token (required) |
| **Authorization** | Only tasks with matching owner_id are returned |
| **Query Parameters** | |
| - `page` (int, optional) | Page number, default: 1 |
| - `per_page` (int, optional) | Items per page, default: 10, max: 100 |
| **Response Format** | `JSON` |
| **Success Response (200)** | TaskList with tasks, total, page, per_page |
| **Security** | Query automatically filtered by current_user.id |

### Feature 6: Root & Status Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check message |
| `/api/status` | GET | API status with framework, database, and auth info |

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
| **JWT** | python-jose | Latest |
| **Password Hashing** | passlib + bcrypt | Latest |
| **Authentication** | OAuth2 Password Flow | Standard |
| **Database** | MySQL | 8.0+ |

### 4.2 Project Structure

```
JWT_Authentication/
├── main.py                  # FastAPI application entry point
├── auth.py                  # JWT and password hashing utilities
├── database.py              # Database configuration and models
├── dependencies.py          # Authentication dependencies
├── schemas.py               # Pydantic schemas
├── routes/
│   ├── auth.py              # Authentication endpoints
│   └── tasks.py             # Protected task endpoints
├── venv/                    # Virtual environment
├── deployment_guide.md      # Deployment instructions
└── prd.md                   # This document
```

### 4.3 Database Schema

#### Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| username | String(50) | UNIQUE, NOT NULL, Indexed |
| email | String(100) | UNIQUE, NOT NULL, Indexed |
| password_hash | String(255) | NOT NULL |
| created_at | DateTime | DEFAULT: UTC now |

#### Tasks Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| title | String(100) | NOT NULL |
| description | String(500) | NULLABLE |
| priority | Enum | DEFAULT: medium |
| completed | Boolean | DEFAULT: False |
| owner_id | Integer | Foreign Key → users.id |
| created_at | DateTime | DEFAULT: UTC now |
| updated_at | DateTime | DEFAULT: UTC now, Auto-update |

### 4.4 Security Implementation

#### Password Security
- **Algorithm**: bcrypt (via passlib)
- **Hashing**: `pwd_context.hash(password)`
- **Verification**: `pwd_context.verify(plain, hashed)`

#### JWT Token Security
- **Algorithm**: HS256
- **Secret Key**: Configurable via environment
- **Access Token Expiry**: 30 minutes
- **Refresh Token Expiry**: 7 days

#### Token Payload
```json
{
  "sub": "user_id",
  "type": "access" | "refresh",
  "exp": "expiry_timestamp"
}
```

---

## 5. Non-Functional Requirements

### 5.1 Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| **Password Storage** | bcrypt hashing (NEVER plaintext) |
| **Token Security** | JWT with expiration |
| **SQL Injection** | SQLAlchemy ORM prevents this |
| **Input Validation** | Pydantic schemas |
| **Credential Exposure** | Environment variables for secrets |

### 5.2 Performance Requirements

- **Authentication Overhead**: <5ms per request
- **Token Generation**: <10ms
- **Database Queries**: <100ms

### 5.3 Error Handling

| Status Code | Scenario |
|-------------|----------|
| 401 | Invalid/missing token |
| 403 | Forbidden (not implemented yet) |
| 404 | Resource not found |
| 409 | Duplicate email/username |
| 422 | Validation error |

---

## 6. User Interactions and Flows

### Flow 1: User Registration
```
User → POST /auth/register
       Body: {"username": "john", "email": "john@example.com", "password": "secret123"}
       → Server validates input
       → Server checks for existing email/username
       → Server hashes password with bcrypt
       → Server creates user in MySQL
       → Server returns 201 with UserResponse
```

### Flow 2: User Login
```
User → POST /auth/login
       Body (form): username=john@example.com&password=secret123
       → Server finds user by email
       → Server verifies password with bcrypt
       → Server generates access and refresh tokens
       → Server returns 200 with TokenResponse
```

### Flow 3: Authenticated Task Creation
```
User → POST /tasks
       Header: Authorization: Bearer <access_token>
       Body: {"title": "My Task", "priority": "high"}
       → Server validates JWT token
       → Server extracts user_id from token
       → Server creates task with owner_id = user_id
       → Server returns 201 with TaskResponse
```

### Flow 4: Viewing User's Tasks
```
User → GET /tasks
       Header: Authorization: Bearer <access_token>
       → Server validates JWT token
       → Server extracts user_id from token
       → Server queries tasks WHERE owner_id = user_id
       → Server returns paginated TaskList
```

---

## 7. Success Metrics

### 7.1 Security Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Password Security** | 0% plaintext passwords | Database inspection |
| **Token Validation** | 100% invalid tokens rejected | Test with forged tokens |
| **Data Isolation** | 100% of tasks with correct owner_id | Query verification |

### 7.2 Functional Metrics

| Metric | Target |
|--------|--------|
| Registration Success | All valid inputs accepted |
| Login Success | Valid credentials return tokens |
| Protected Routes | Require valid Bearer token |
| User Isolation | Users only see their own tasks |

### 7.3 Performance Metrics

| Metric | Target |
|--------|--------|
| Authentication Latency | <5ms |
| Token Generation | <10ms |
| Protected Request | <100ms total |

---

## 8. Future Enhancements

### Phase 2: Enhanced Security
- [ ] Add refresh token rotation
- [ ] Implement token revocation/blacklisting
- [ ] Add email verification
- [ ] Implement password reset flow

### Phase 3: Extended Task Features
- [ ] PUT/PATCH/DELETE endpoints for tasks
- [ ] Task categories and labels
- [ ] Due dates and reminders

### Phase 4: Advanced Features
- [ ] Role-based access control (RBAC)
- [ ] API key authentication
- [ ] Rate limiting per user

### Phase 5: DevOps
- [ ] CI/CD pipeline
- [ ] Docker containerization
- [ ] Multi-factor authentication (MFA)

---

## 9. Environment Configuration

### 9.1 Required Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| SECRET_KEY | (change in production) | JWT signing key |
| DB_USER | root | MySQL username |
| DB_PASSWORD | teja12345 | MySQL password |
| DB_HOST | localhost | Database host |
| DB_PORT | 3306 | Database port |
| DB_NAME | tasks_db | Database name |

### 9.2 Security Note

> [!IMPORTANT]
> The `SECRET_KEY` in [`auth.py`](auth.py:6) must be changed before deploying to any public-facing server. Use a strong, randomly generated key and store it in environment variables.

---

## 10. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Weak JWT secret | Medium | Critical | Use strong keys, rotate periodically |
| Token leakage | Medium | High | Short expiry, refresh token rotation |
| SQL injection | Low | High | SQLAlchemy ORM prevents this |
| Password breach | Low | Critical | bcrypt with proper work factor |
| Data isolation bypass | Low | Critical | Verify owner_id in all queries |

---

## 11. Glossary

| Term | Definition |
|------|------------|
| **JWT** | JSON Web Token - compact, URL-safe token format |
| **OAuth2** | Open Authorization 2.0 - authorization framework |
| **Bearer Token** | Token type where the client presents the token |
| **Bcrypt** | Password hashing algorithm |
| **Pydantic** | Data validation library |
| **Dependency Injection** | Design pattern for providing dependencies |
| **HS256** | HMAC-SHA256 - JWT signing algorithm |

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
