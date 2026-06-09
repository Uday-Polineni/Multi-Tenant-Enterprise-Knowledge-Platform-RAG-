import json
import logging
import uuid

from app.core.config import get_settings
from app.core.redis_client import redis_or_none
from app.schemas.query import QueryResponse
from app.services.cache_keys import (
    answer_cache_key,
    embedding_cache_key,
    org_cache_version_key,
)
from app.services.semantic_cache import (
    find_semantic_cached_answer,
    store_semantic_cached_answer,
)

logger = logging.getLogger(__name__)


def get_org_cache_version(*, organization_id: uuid.UUID) -> int:
    client = redis_or_none()
    if client is None:
        return 0

    key = org_cache_version_key(organization_id)
    try:
        value = client.get(key)
        if value is None:
            return 0
        return int(value)
    except Exception:
        logger.exception("Failed to read org cache version for %s", organization_id)
        return 0


def bump_org_cache_version(*, organization_id: uuid.UUID) -> int:
    """Advance org cache version so new reads miss stale versioned keys."""
    client = redis_or_none()
    if client is None:
        return 0

    key = org_cache_version_key(organization_id)
    try:
        return int(client.incr(key))
    except Exception:
        logger.exception("Failed to bump org cache version for %s", organization_id)
        return 0


def _delete_keys_matching(client, pattern: str) -> int:
    deleted = 0
    try:
        for key in client.scan_iter(match=pattern, count=200):
            client.delete(key)
            deleted += 1
    except Exception:
        logger.exception("Failed to delete cache keys matching %s", pattern)
    return deleted


def purge_org_query_cache(*, organization_id: uuid.UUID) -> None:
    """Delete exact + semantic answer cache entries for an org, then bump version."""
    client = redis_or_none()
    if client is None:
        return

    org_id = str(organization_id)
    patterns = (
        f"cache:answer:{org_id}:*",
        f"cache:semantic:{org_id}:*",
    )
    try:
        for pattern in patterns:
            removed = _delete_keys_matching(client, pattern)
            if removed:
                logger.info(
                    "Purged %d cache key(s) for org %s pattern %s",
                    removed,
                    organization_id,
                    pattern,
                )
    except Exception:
        logger.exception("Failed to purge query cache for org %s", organization_id)

    bump_org_cache_version(organization_id=organization_id)


def get_cached_answer(
    *,
    organization_id: uuid.UUID,
    role: str,
    question: str,
) -> QueryResponse | None:
    client = redis_or_none()
    if client is None:
        return None

    cache_version = get_org_cache_version(organization_id=organization_id)
    key = answer_cache_key(
        organization_id=organization_id,
        role=role,
        question=question,
        cache_version=cache_version,
    )
    try:
        raw = client.get(key)
        if raw is None:
            return None
        return QueryResponse.model_validate_json(raw)
    except Exception:
        logger.exception("Failed to read answer cache for key %s", key)
        return None


def get_semantic_cache_hit(
    *,
    organization_id: uuid.UUID,
    role: str,
    query_embedding: list[float],
):
    cache_version = get_org_cache_version(organization_id=organization_id)
    return find_semantic_cached_answer(
        organization_id=organization_id,
        role=role,
        cache_version=cache_version,
        query_embedding=query_embedding,
    )


def set_cached_answer(
    *,
    organization_id: uuid.UUID,
    role: str,
    question: str,
    response: QueryResponse,
    query_embedding: list[float] | None = None,
    retrieved_chunk_ids: list[str] | None = None,
    allow_semantic_cache: bool = True,
) -> None:
    client = redis_or_none()
    if client is None:
        return

    settings = get_settings()
    cache_version = get_org_cache_version(organization_id=organization_id)
    key = answer_cache_key(
        organization_id=organization_id,
        role=role,
        question=question,
        cache_version=cache_version,
    )
    try:
        client.setex(key, settings.cache_ttl_seconds, response.model_dump_json())
    except Exception:
        logger.exception("Failed to write answer cache for key %s", key)

    if (
        allow_semantic_cache
        and query_embedding is not None
        and retrieved_chunk_ids is not None
    ):
        store_semantic_cached_answer(
            organization_id=organization_id,
            role=role,
            cache_version=cache_version,
            question=question,
            query_embedding=query_embedding,
            response=response,
            retrieved_chunk_ids=retrieved_chunk_ids,
        )


def get_cached_embedding(question: str) -> list[float] | None:
    client = redis_or_none()
    if client is None:
        return None

    key = embedding_cache_key(question)
    try:
        raw = client.get(key)
        if raw is None:
            return None
        data = json.loads(raw)
        if isinstance(data, list):
            return [float(value) for value in data]
        return None
    except Exception:
        logger.exception("Failed to read embedding cache for key %s", key)
        return None


def set_cached_embedding(question: str, embedding: list[float]) -> None:
    client = redis_or_none()
    if client is None:
        return

    settings = get_settings()
    key = embedding_cache_key(question)
    try:
        client.setex(key, settings.cache_ttl_seconds, json.dumps(embedding))
    except Exception:
        logger.exception("Failed to write embedding cache for key %s", key)


# Used by document upload, update, delete, and embed-complete lifecycle
def invalidate_org_answer_cache(*, organization_id: uuid.UUID) -> None:
    purge_org_query_cache(organization_id=organization_id)
