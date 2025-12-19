import json
from typing import Any, Iterable

from prometheus_client import Counter

try:
    from redis import Redis
    from redis.exceptions import RedisError

    REDIS_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency for local dev
    Redis = Any  # type: ignore
    REDIS_AVAILABLE = False

    class RedisError(Exception):
        """Fallback error class when redis package is unavailable."""


from app.core.config import get_settings

settings = get_settings()
_cache_client: Redis | None = None

cache_hits = Counter(
    "cache_hits_total", "Number of cache hits for cached responses", ["endpoint"]
)
cache_misses = Counter(
    "cache_misses_total", "Number of cache misses for cached responses", ["endpoint"]
)


def get_cache_client() -> Redis | None:
    global _cache_client
    if not REDIS_AVAILABLE:
        return None
    if _cache_client is not None:
        return _cache_client

    try:
        _cache_client = Redis.from_url(settings.redis_url, decode_responses=True)
        _cache_client.ping()
    except RedisError:
        _cache_client = None

    return _cache_client


def get_cached_response(key: str, endpoint: str) -> Any | None:
    client = get_cache_client()
    if not client:
        return None

    try:
        cached_value = client.get(key)
    except RedisError:
        return None

    if cached_value is None:
        cache_misses.labels(endpoint=endpoint).inc()
        return None

    cache_hits.labels(endpoint=endpoint).inc()
    try:
        return json.loads(cached_value)
    except json.JSONDecodeError:
        return None


def set_cached_response(key: str, value: Any, ttl_seconds: int | None = None) -> None:
    client = get_cache_client()
    if not client:
        return

    try:
        client.setex(key, ttl_seconds or settings.cache_ttl_seconds, json.dumps(value, default=str))
    except RedisError:
        return


def invalidate_cache(keys: Iterable[str]) -> None:
    client = get_cache_client()
    if not client:
        return

    try:
        client.delete(*keys)
    except RedisError:
        return
