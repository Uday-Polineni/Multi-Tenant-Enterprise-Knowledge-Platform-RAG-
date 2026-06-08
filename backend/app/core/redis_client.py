import logging
from functools import lru_cache

import redis

from app.core.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache
def get_redis_client() -> redis.Redis:
    settings = get_settings()
    return redis.from_url(settings.redis_url, decode_responses=True)


def is_redis_available() -> bool:
    try:
        get_redis_client().ping()
        return True
    except redis.RedisError:
        return False


def redis_or_none() -> redis.Redis | None:
    if not is_redis_available():
        logger.warning("Redis unavailable — skipping cache, rate limit, and async queue")
        return None
    return get_redis_client()
