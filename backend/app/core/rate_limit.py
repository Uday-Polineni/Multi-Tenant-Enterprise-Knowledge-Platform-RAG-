import logging
import uuid

from app.core.config import get_settings
from app.core.redis_client import redis_or_none

logger = logging.getLogger(__name__)

RATE_LIMIT_WINDOW_SECONDS = 3600


class RateLimitExceeded(Exception):
    pass


def check_rate_limit(*, organization_id: uuid.UUID, user_id: uuid.UUID) -> None:
    client = redis_or_none()
    if client is None:
        return

    settings = get_settings()
    key = f"rl:{organization_id}:{user_id}"
    try:
        count = client.incr(key)
        if count == 1:
            client.expire(key, RATE_LIMIT_WINDOW_SECONDS)
        if count > settings.rate_limit_per_hour:
            raise RateLimitExceeded(
                f"Rate limit exceeded ({settings.rate_limit_per_hour} requests per hour)"
            )
    except RateLimitExceeded:
        raise
    except Exception:
        logger.exception("Rate limit check failed for %s", key)
