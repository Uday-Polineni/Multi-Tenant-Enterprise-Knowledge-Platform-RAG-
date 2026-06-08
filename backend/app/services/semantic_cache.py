import json
import logging
import uuid
from dataclasses import dataclass

from app.core.config import get_settings
from app.core.redis_client import redis_or_none
from app.schemas.query import QueryResponse
from app.services.cache_keys import normalize_question, semantic_cache_index_key

logger = logging.getLogger(__name__)


@dataclass
class SemanticCacheHit:
    response: QueryResponse
    retrieved_chunk_ids: list[str]
    similarity: float


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or not left:
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    norm_left = sum(a * a for a in left) ** 0.5
    norm_right = sum(b * b for b in right) ** 0.5
    if norm_left == 0.0 or norm_right == 0.0:
        return 0.0
    return dot / (norm_left * norm_right)


def find_semantic_cached_answer(
    *,
    organization_id: uuid.UUID,
    role: str,
    cache_version: int,
    query_embedding: list[float],
) -> SemanticCacheHit | None:
    settings = get_settings()
    if not settings.semantic_cache_enabled:
        return None

    client = redis_or_none()
    if client is None:
        return None

    index_key = semantic_cache_index_key(
        organization_id=organization_id,
        role=role,
        cache_version=cache_version,
    )
    try:
        raw_entries = client.lrange(index_key, 0, -1)
    except Exception:
        logger.exception("Failed to read semantic cache index %s", index_key)
        return None

    best: SemanticCacheHit | None = None
    threshold = settings.semantic_cache_similarity_threshold

    for raw in raw_entries:
        try:
            data = json.loads(raw)
            embedding = data.get("embedding")
            response_raw = data.get("response")
            chunk_ids = data.get("retrieved_chunk_ids", [])
            if not isinstance(embedding, list) or not response_raw:
                continue
            embedding = [float(value) for value in embedding]
            similarity = cosine_similarity(query_embedding, embedding)
            if similarity < threshold:
                continue
            if best is not None and similarity <= best.similarity:
                continue
            response = QueryResponse.model_validate(response_raw)
            best = SemanticCacheHit(
                response=response,
                retrieved_chunk_ids=[str(value) for value in chunk_ids],
                similarity=similarity,
            )
        except Exception:
            logger.exception("Skipping invalid semantic cache entry")
            continue

    return best


def store_semantic_cached_answer(
    *,
    organization_id: uuid.UUID,
    role: str,
    cache_version: int,
    question: str,
    query_embedding: list[float],
    response: QueryResponse,
    retrieved_chunk_ids: list[str],
) -> None:
    settings = get_settings()
    if not settings.semantic_cache_enabled:
        return

    client = redis_or_none()
    if client is None:
        return

    index_key = semantic_cache_index_key(
        organization_id=organization_id,
        role=role,
        cache_version=cache_version,
    )
    payload = json.dumps(
        {
            "question": normalize_question(question),
            "embedding": query_embedding,
            "response": response.model_dump(mode="json"),
            "retrieved_chunk_ids": retrieved_chunk_ids,
        }
    )
    try:
        pipe = client.pipeline()
        pipe.lpush(index_key, payload)
        pipe.ltrim(index_key, 0, settings.semantic_cache_max_entries - 1)
        pipe.expire(index_key, settings.cache_ttl_seconds)
        pipe.execute()
    except Exception:
        logger.exception("Failed to write semantic cache entry to %s", index_key)
