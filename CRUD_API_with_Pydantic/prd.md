# Product Requirements Document (PRD) - "CRUD API with Pydantic"

## Project Overview
A standard Task Management API demonstrating best practices in data validation using Pydantic and asynchronous database interaction with SQLAlchemy.

## Objectives
- Provide full CRUD (Create, Read, Update, Delete) capabilities for task management.
- Ensure strict data integrity through Pydantic schemas and custom validators.
- Support paginated list views for efficient data handling.

## Core Features
1. **Task Creation (`POST /tasks`)**
   - **User Story**: As a user, I want to create a task with a title, description, and priority.
   - **Validation**: Title must be 1-100 characters and not empty.
2. **Task Retrieval (`GET /tasks`)**
   - **User Story**: As a user, I want to see all my tasks with support for pagination.
3. **Task Updates (`PATCH /tasks/{id}`)**
   - **User Story**: As a user, I want to update specific fields of a task (e.g., mark it as completed).
4. **Task Deletion (`DELETE /tasks/{id}`)**

## Technical Requirements
- **Framework**: FastAPI
- **Validation**: Pydantic v2
- **Database**: MySQL (Async via `aiomysql`)
- **Documentation**: Automatic Swagger UI at `/docs`.

## Success Metrics
- 100% rejection of malformed data before reaching the database.
- Scalable pagination supporting thousands of tasks.
