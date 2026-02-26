# Product Requirements Document (PRD) - "JWT Authentication API"

## Project Overview
A secure, multi-user task management foundation featuring robust authentication via JSON Web Tokens (JWT) and persistent user profiles.

## Objectives
- Secure all sensitive endpoints behind authentication.
- Implement user-specific data ownership (users only see their own tasks).
- Provide industry-standard password security (bcrypt hashing).
- Support scalable authentication via stateless tokens.

## Core Features
1. **User Registration & Login (`POST /register`, `POST /login`)**
   - **User Story**: As a new user, I want to create an account and receive a token for further access.
2. **JWT Issuance & Refresh**
   - **Mechanism**: Access tokens (30 mins) for API calls, Refresh tokens (7 days) for session maintenance.
3. **Protected Task Management**
   - **User Story**: As a logged-in user, I want to manage my personal tasks privately.
   - **Enforcement**: Middleware validates the `Authorization: Bearer <token>` header on every request.
4. **User Profile Retrieval**
   - **User Story**: As a user, I want to see my registered details.

## Technical Requirements
- **Framework**: FastAPI
- **Security**: `python-jose` (JWT), `passlib` (Bcrypt)
- **Database**: MySQL (with Foreign Key relations between Users and Tasks)
- **Documentation**: Automatic Swagger UI at `/docs`.

## Success Metrics
- 100% of tasks associated with the correct `owner_id`.
- Zero plaintext passwords stored in the database.
- Average authentication overhead < 5ms per request.
