import logging
import uuid

from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import get_settings
from app.core.redis_client import is_redis_available

logger = logging.getLogger(__name__)


async def enqueue_embed_document(
    *,
    document_id: uuid.UUID,
    organization_id: uuid.UUID,
) -> bool:
    if not is_redis_available():
        logger.warning("Cannot enqueue embed job — Redis unavailable")
        return False

    settings = get_settings()
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    pool = await create_pool(redis_settings)
    try:
        await pool.enqueue_job(
            "embed_document_task",
            str(document_id),
            str(organization_id),
        )
        return True
    except Exception:
        logger.exception("Failed to enqueue embed job for document %s", document_id)
        return False
    finally:
        await pool.aclose()
