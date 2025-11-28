import redis
import json
import os
from functools import wraps
from flask import current_app

# Initialize Redis client connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    decode_responses=True  # Automatically decode byte responses to strings
)

def cache_key(prefix, *args):
    """Generate a cache key string from prefix and arguments"""
    return f"{prefix}:{':'.join(str(arg) for arg in args)}"

def cache_get(key):
    """Retrieve value from Redis cache by key"""
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        current_app.logger.error(f"Cache get error: {e}")
        return None

def cache_set(key, value, expire=300):
    """Store value in Redis cache with expiration time (default 5 minutes)"""
    try:
        redis_client.setex(key, expire, json.dumps(value))
        return True
    except Exception as e:
        current_app.logger.error(f"Cache set error: {e}")
        return False

def cache_delete(key):
    """Remove a specific key from Redis cache"""
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        current_app.logger.error(f"Cache delete error: {e}")
        return False

def cache_clear_pattern(pattern):
    """Delete all cache keys matching a given pattern (e.g., "api:lots*")"""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        current_app.logger.error(f"Cache clear pattern error: {e}")
        return False

def cached(expire=300, key_prefix="default"):
    """Decorator to automatically cache function results in Redis"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate unique cache key from function name and arguments
            cache_key_name = cache_key(key_prefix, func.__name__, *args, *kwargs.values())
            
            # Check if result exists in cache
            cached_result = cache_get(cache_key_name)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache the result
            result = func(*args, **kwargs)
            cache_set(cache_key_name, result, expire)
            return result
        return wrapper
    return decorator