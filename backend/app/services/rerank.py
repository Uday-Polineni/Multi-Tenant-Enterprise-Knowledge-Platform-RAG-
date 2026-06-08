from app.core.ai.bge_reranker import get_reranker_provider
from app.core.config import get_settings
from app.services.vector_store import ChunkSearchResult


def rerank_hits(
    *,
    question: str,
    hits: list[ChunkSearchResult],
    top_n: int | None = None,
) -> list[ChunkSearchResult]:
    if not hits:
        return []

    settings = get_settings()
    limit = top_n if top_n is not None else settings.rag_rerank_top_n
    if limit <= 0:
        return []

    if not settings.reranker_enabled:
        return hits[:limit]

    ranked_indices = get_reranker_provider().rerank(
        question,
        [hit.content for hit in hits],
    )
    return [hits[index] for index in ranked_indices[:limit]]
