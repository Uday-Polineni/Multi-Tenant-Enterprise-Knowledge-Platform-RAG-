import re
import uuid

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.chunk import search_chunks_fulltext
from app.services.query_routing import extract_audit_token
from app.services.vector_store import ChunkSearchResult, search

_COMMON_CAP_WORDS = frozenset({
    "How", "What", "When", "Where", "Who", "Why", "Can", "Will", "The", "This",
    "That", "And", "Or", "But", "For", "With", "From", "Are", "Was", "Were",
})


def supplementary_fts_queries(question: str) -> list[str]:
    """Extra FTS queries when terms live in different documents (e.g. a name vs a topic)."""
    queries: list[str] = []
    lower = question.lower()

    for match in re.finditer(r"\b([A-Z][a-z]{2,})\b", question):
        word = match.group(1)
        if word not in _COMMON_CAP_WORDS:
            queries.append(word)

    for term in ("portfolio", "resume", "developer", "weekend", "build"):
        if term in lower:
            queries.append(term)

    if "portfolio" in lower and "developer" in lower:
        queries.extend(["JavaScript", "TypeScript", "React"])

    for cert_id in re.findall(r"CERT-[a-z]+-\d+", question, re.IGNORECASE):
        queries.append(cert_id)

    audit_token = extract_audit_token(question)
    if audit_token:
        queries.append(audit_token)

    page_match = re.search(r"\bpage\s+(\d+)\b", question, re.IGNORECASE)
    if page_match:
        queries.append(f"PAGE {page_match.group(1)}")

    for pdf_name in re.findall(r"[\w-]+\.pdf", question, re.IGNORECASE):
        queries.append(pdf_name.replace(".pdf", "").replace("_", " "))

    seen: set[str] = set()
    deduped: list[str] = []
    for query in queries:
        key = query.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(query)
    return deduped


def reciprocal_rank_fusion(
    ranked_lists: list[list[uuid.UUID]],
    *,
    k: int,
    top_n: int,
) -> list[uuid.UUID]:
    scores: dict[uuid.UUID, float] = {}
    for ranked in ranked_lists:
        for rank, chunk_id in enumerate(ranked, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + rank)

    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [chunk_id for chunk_id, _ in ordered[:top_n]]


def hybrid_retrieve(
    db: Session,
    *,
    organization_id: uuid.UUID,
    question: str,
    query_embedding: list[float],
    allowed_access_levels: list[str],
    top_k: int,
    document_ids: list[uuid.UUID] | None = None,
    page_number: int | None = None,
    audit_token: str | None = None,
) -> tuple[list[ChunkSearchResult], dict[str, int]]:
    settings = get_settings()
    timings: dict[str, int] = {}

    import time

    t0 = time.perf_counter()
    vector_hits = search(
        organization_id=organization_id,
        query_embedding=query_embedding,
        top_k=top_k,
        allowed_access_levels=allowed_access_levels,
        document_ids=document_ids,
        page_number=page_number,
    )
    timings["chroma_ms"] = int((time.perf_counter() - t0) * 1000)

    if not settings.hybrid_search_enabled:
        timings["bm25_ms"] = 0
        timings["rrf_ms"] = 0
        return vector_hits, timings

    t0 = time.perf_counter()
    fts_lists = _collect_fts_ranked_lists(
        db,
        organization_id=organization_id,
        question=question,
        allowed_access_levels=allowed_access_levels,
        top_k=top_k,
        document_ids=document_ids,
        page_number=page_number,
        audit_token=audit_token,
    )
    timings["bm25_ms"] = int((time.perf_counter() - t0) * 1000)

    if not vector_hits and not fts_lists:
        timings["rrf_ms"] = 0
        return [], timings

    if not fts_lists:
        timings["rrf_ms"] = 0
        return vector_hits, timings

    if not vector_hits:
        timings["rrf_ms"] = 0
        return fts_lists[0][:top_k], timings

    t0 = time.perf_counter()
    ranked_lists = [[hit.chunk_id for hit in vector_hits]]
    ranked_lists.extend([hit.chunk_id for hit in fts_list] for fts_list in fts_lists)
    fused_ids = reciprocal_rank_fusion(
        ranked_lists,
        k=settings.hybrid_rrf_k,
        top_n=top_k,
    )
    hits = _merge_hit_lists_from_sources(
        fused_ids,
        vector_hits=vector_hits,
        fts_lists=fts_lists,
    )
    timings["rrf_ms"] = int((time.perf_counter() - t0) * 1000)
    return hits, timings


def _collect_fts_ranked_lists(
    db: Session,
    *,
    organization_id: uuid.UUID,
    question: str,
    allowed_access_levels: list[str],
    top_k: int,
    document_ids: list[uuid.UUID] | None = None,
    page_number: int | None = None,
    audit_token: str | None = None,
) -> list[list[ChunkSearchResult]]:
    lists: list[list[ChunkSearchResult]] = []
    seen_queries: set[str] = set()
    leading_queries: list[str] = []
    if audit_token:
        leading_queries.append(audit_token)

    for query in [*leading_queries, question, *supplementary_fts_queries(question)]:
        key = query.strip().lower()
        if not key or key in seen_queries:
            continue
        seen_queries.add(key)

        hits = search_chunks_fulltext(
            db,
            organization_id=organization_id,
            question=query,
            allowed_access_levels=allowed_access_levels,
            top_k=top_k,
            document_ids=document_ids,
            page_number=page_number,
            audit_token=audit_token if page_number is not None else None,
        )
        if hits:
            lists.append(hits)

    return lists


def _merge_hit_lists_from_sources(
    chunk_ids: list[uuid.UUID],
    *,
    vector_hits: list[ChunkSearchResult],
    fts_lists: list[list[ChunkSearchResult]],
) -> list[ChunkSearchResult]:
    by_id: dict[uuid.UUID, ChunkSearchResult] = {}
    for hit in vector_hits:
        by_id[hit.chunk_id] = hit
    for fts_hits in fts_lists:
        for hit in fts_hits:
            by_id.setdefault(hit.chunk_id, hit)

    return [by_id[chunk_id] for chunk_id in chunk_ids if chunk_id in by_id]
