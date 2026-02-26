# Product Requirements Document (PRD) - "Async API Aggregator"

## 1. Project Overview

### Project Name
Async API Aggregator

### Project Type
High-Performance API Aggregation Service

### Project Description
A performance-oriented backend service designed to aggregate data from multiple third-party APIs (Weather and News) concurrently using Python's asyncio. The service implements intelligent caching with TTL (Time To Live) to minimize latency and reduce external API calls.

### Target Users
- **Primary**: Developers learning async patterns and API aggregation
- **Secondary**: Applications needing unified access to multiple data sources

---

## 2. Objectives

### Business Objectives
1. Implement concurrent data fetching using `asyncio.gather`
2. Provide a unified response format for multiple data sources
3. Minimize external API calls through memory-efficient caching
4. Demonstrate high-performance async patterns

### Learning Objectives
- Master Python asyncio and concurrent programming
- Understand TTL caching strategies
- Learn API client patterns with httpx
- Implement error handling in async contexts

---

## 3. Core Features

### Feature 1: Aggregated City Data (`GET /aggregate/{city}`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `GET /aggregate/{city}` |
| **Description** | Fetch weather and news data for a city concurrently |
| **User Story** | As a user, I want to see weather and news for a specific city in a single request |
| **Path Parameters** | |
| - `city` (string, required) | Name of the city |
| **Query Parameters** | |
| - `no_cache` (bool, optional) | Force fresh data (default: false) |
| **Response Format** | `JSON` |
| **Success Response (200)** | Combined weather and news data |
| **Caching** | 5-minute TTL (300 seconds) |
| **Cache Key** | `aggregate:{city.lower()}` |
| **Response Headers** | |
| - `X-Cache` | "HIT" or "MISS" |

### Feature 2: Cache Management (`DELETE /aggregate/cache`)

| Attribute | Details |
|-----------|---------|
| **Endpoint** | `DELETE /aggregate/cache` |
| **Description** | Clear all cached data |
| **User Story** | As an admin, I want to clear the system cache manually |
| **Response Format** | `JSON` |
| **Success Response (200)** | `{"message": "Cache cleared"}` |
| **Action** | Clears all items from in-memory cache |

### Feature 3: Weather Data Fetching (Internal)

| Attribute | Details |
|-----------|---------|
| **Function** | `fetch_weather(city)` |
| **Data Source** | OpenWeatherMap API |
| **API Endpoint** | `/weather` |
| **Response Fields** | |
| - `source` | "weather" |
| - `status` | "ok" or "simulated" |
| - `data.temp` | Temperature in Celsius |
| - `data.description` | Weather description |
| - `data.city` | City name |
| **Error Handling** | Returns simulated data if API key invalid |
| **Fallback** | Simulated response with 0.5s delay |

### Feature 4: News Data Fetching (Internal)

| Attribute | Details |
|-----------|---------|
| **Function** | `fetch_news(city)` |
| **Data Source** | NewsAPI (simulated) |
| **Response Fields** | |
| - `source` | "news" |
| - `status` | "ok" |
| - `data` | Array of news articles |
| **Note** | Currently simulated with 0.8s delay |

### Feature 5: Root & Status Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check message |
| `/api/status` | GET | API status with features list |

---

## 4. Technical Requirements

### 4.1 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Language** | Python | 3.12+ |
| **Web Framework** | FastAPI | Latest stable |
| **ASGI Server** | Uvicorn | Latest stable |
| **HTTP Client** | httpx | Latest (async) |
| **Caching** | cachetools (TTLCache) | Latest |
| **Concurrency** | asyncio | Built-in |

### 4.2 Project Structure

```
Async_API _aggregator/
├── main.py                  # FastAPI application entry point
├── clients.py               # API clients for external services
├── cache.py                # Cache configuration
├── routers/
│   └── aggregate.py         # Aggregation endpoints
├── venv/                   # Virtual environment
├── deployment_guide.md      # Deployment instructions
└── prd.md                  # This document
```

### 4.3 Caching Configuration

| Setting | Value |
|---------|-------|
| **Cache Type** | TTLCache (in-memory) |
| **Max Size** | 100 items |
| **TTL** | 300 seconds (5 minutes) |
| **Key Format** | `aggregate:{city}` |

### 4.4 Concurrency Implementation

```python
# Using asyncio.gather for concurrent execution
results = await asyncio.gather(
    fetch_weather(city),
    fetch_news(city),
    return_exceptions=True
)
```

**Benefits:**
- Total time ≈ max(time_weather, time_news) instead of sum
- Non-blocking I/O operations
- Efficient resource utilization

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

| Metric | Target | Notes |
|--------|--------|-------|
| **Cache Hit Response** | <50ms | Served from memory |
| **Cache Miss Response** | <1000ms | Concurrent API calls |
| **Concurrency Gain** | ~50% faster | vs sequential calls |
| **Cache TTL** | 5 minutes | Configurable |

### 5.2 Scalability Considerations

| Aspect | Current | Future |
|--------|---------|--------|
| **Cache** | In-memory (single instance) | Redis for distributed |
| **Workers** | Single/multiple uvicorn | Kubernetes auto-scaling |
| **External APIs** | Rate limited | Implement rate limiting |

### 5.3 Error Handling

| Scenario | Behavior |
|----------|----------|
| API timeout | Return partial results with error |
| Invalid API key | Use simulated fallback data |
| Cache full | Evict oldest entries (LRU) |
| Invalid city | Return 404 or empty results |

---

## 6. User Interactions and Flows

### Flow 1: Aggregated City Data
```
User → GET /aggregate/London
       ↓
Server checks cache (cache_key = "aggregate:london")
       ↓
If MISS: Execute fetch_weather() + fetch_news() concurrently
       ↓
Return combined response:
{
  "city": "London",
  "results": [weather_data, news_data],
  "timing_ms": 823.5,
  "sources_ok": 2
}
       ↓
Cache result with 5-minute TTL
```

### Flow 2: Cached Response
```
User → GET /aggregate/London (within 5 minutes)
       ↓
Server finds cache HIT
       ↓
Return cached response immediately
       ↓
Response header: X-Cache: HIT
```

### Flow 3: Force Fresh Data
```
User → GET /aggregate/London?no_cache=true
       ↓
Server ignores cache
       ↓
Fetches fresh data from APIs
       ↓
Response header: X-Cache: MISS
```

### Flow 4: Clear Cache
```
User → DELETE /aggregate/cache
       ↓
Server clears all cached items
       ↓
Return: {"message": "Cache cleared"}
```

---

## 7. Success Metrics

### 7.1 Performance Metrics

| Metric | Target |
|--------|--------|
| Cache hit response time | <50ms |
| Concurrent execution time | <1000ms |
| Cache hit rate | >70% (after warmup) |

### 7.2 Functional Metrics

| Metric | Target |
|--------|--------|
| Both APIs fetched concurrently | Yes |
| Cache properly expires | TTL respected |
| Manual cache clear works | 100% |

### 7.3 Code Quality

| Metric | Target |
|--------|--------|
| Async/await usage | All I/O operations |
| Error handling | Graceful fallbacks |
| Type hints | All functions |

---

## 8. Future Enhancements

### Phase 2: Real API Integration
- [ ] Implement actual OpenWeatherMap API key
- [ ] Implement actual NewsAPI integration
- [ ] Add more data sources (sports, stocks, etc.)

### Phase 3: Advanced Caching
- [ ] Replace TTLCache with Redis
- [ ] Add cache invalidation webhooks
- [ ] Implement distributed caching

### Phase 4: Production Features
- [ ] Add rate limiting per API
- [ ] Implement API key rotation
- [ ] Add request queuing
- [ ] CI/CD pipeline

### Phase 5: Scaling
- [ ] Kubernetes deployment
- [ ] Auto-scaling configuration
- [ ] Load balancing

---

## 9. API Keys Configuration

### 9.1 Required API Keys

| Service | Environment Variable | Purpose |
|---------|---------------------|---------|
| OpenWeatherMap | `OPENWEATHER_API_KEY` | Weather data |

### 9.2 Setting API Keys

```bash
# Set environment variable
export OPENWEATHER_API_KEY=your_api_key_here
```

### 9.3 Fallback Behavior

If no valid API key is provided:
- Weather returns simulated data
- System continues to function
- Logs warning message

---

## 10. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| External API downtime | Medium | Medium | Use simulated fallbacks |
| Cache memory growth | Low | Low | TTLCache auto-evicts |
| Rate limiting | Medium | Medium | Implement queuing |
| In-memory cache (multi-instance) | Medium | Medium | Move to Redis |

---

## 11. Glossary

| Term | Definition |
|------|------------|
| **Asyncio** | Python library for writing concurrent code using async/await |
| **asyncio.gather** | Run coroutines concurrently |
| **TTLCache** | Cache that automatically evicts items after TTL |
| **Cache Hit** | Request served from cache |
| **Cache Miss** | Cache expired/not found |
| **Concurrent** | Multiple operations running simultaneously |
| **HTTPX** | Async HTTP client for Python |
| **API Aggregation** | Combining data from multiple sources |

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
