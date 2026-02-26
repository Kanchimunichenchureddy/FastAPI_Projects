# Product Requirements Document (PRD) - "Async API Aggregator"

## Project Overview
A performance-oriented backend service designed to aggregate data from multiple third-party APIs (Weather and News) concurrently, with built-in TTL caching to reduce latency and API hitting.

## Objectives
- Implement concurrent data fetching using `asyncio.gather`.
- Provide a unified response format for multiple data sources.
- Minimize external API calls through memory-efficient caching (`cachetools`).

## Core Features
1. **Aggregated City Data (`/aggregate/{city}`)**
   - **User Story**: As a user, I want to see weather and news for a specific city in a single request.
   - **Mechanism**: Concurrent async calls to OpenWeather and NewsAPI.
   - **Caching**: Results are cached for 5 minutes (TTL).
   - **Cache Control**: `no_cache` query parameter to force fresh data.
2. **Cache Management (`DELETE /aggregate/cache`)**
   - **User Story**: As an admin, I want to clear the system cache manually.
3. **Status Monitoring (`/api/status`)**
   - Provides system health and active features.

## Technical Requirements
- **Framework**: FastAPI
- **Concurrency**: `asyncio` + `httpx`
- **Caching**: `cachetools.TTLCache` (max 100 items, 300s TTL)
- **Documentation**: Automatic Swagger UI at `/docs`.

## Success Metrics
- Average response time < 50ms for cached hits.
- Concurrency prevents response time from being additive (total time ~ max time of single slowest source).
