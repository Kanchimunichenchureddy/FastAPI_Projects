import json
import functools
import redis.asyncio as redis
from fastapi import Request, Response
from typing import Optional

# Redis configuration
REDIS_URL = "redis://localhost:6379"
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def cache_response(ttl: int = 600):
    """
    Decorator to cache FastAPI response in Redis.
    The cache key is based on the request URL path and query parameters.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Find the request object in the arguments
            request: Optional[Request] = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            # If no request object found, we can't easily cache by URL
            if not request:
                return await func(*args, **kwargs)

            cache_key = f"cache:{request.url.path}:{request.url.query}"
            
            # Try to get from cache
            try:
                cached_val = await redis_client.get(cache_key)
                if cached_val:
                    # If we have a response object, set a custom header
                    if "response" in kwargs and isinstance(kwargs["response"], Response):
                        kwargs["response"].headers["X-Cache"] = "HIT"
                    return json.loads(cached_val)
            except Exception as e:
                print(f"Redis get error: {e}")

            # Execute the function
            result = await func(*args, **kwargs)

            # Store in cache
            try:
                await redis_client.setex(cache_key, ttl, json.dumps(result))
                if "response" in kwargs and isinstance(kwargs["response"], Response):
                    kwargs["response"].headers["X-Cache"] = "MISS"
            except Exception as e:
                print(f"Redis set error: {e}")
                if "response" in kwargs and isinstance(kwargs["response"], Response):
                    kwargs["response"].headers["X-Cache"] = "ERROR"

            return result

        return wrapper
    return decorator
