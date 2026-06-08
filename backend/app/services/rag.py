import json
import logging
import re
import threading
import time
import uuid
from collections.abc import Iterator
from dataclasses import replace

from sqlalchemy.orm import Session

from app.core.access import allowed_levels_for_role
from app.core.ai.openai_embedding import get_embedding_provider
from app.core.ai.openai_llm import get_llm_provider
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.repositories.chunk import chunks_exist_for_org
from app.repositories.query_log import create_query_log
from app.schemas.query import Citation, QueryResponse
from app.services.cache import (
    get_cached_answer,
    get_cached_embedding,
    get_semantic_cache_hit,
    set_cached_answer,
    set_cached_embedding,
)
from app.services.hybrid_search import hybrid_retrieve
from app.services.rerank import rerank_hits
from app.services.vector_store import (
    ChunkSearchResult,
    VectorIndexCorruptedError,
    rebuild_org_vector_index,
)

logger = logging.getLogger(__name__)

NO_CONTEXT_ANSWER = (
    "The information is not available in the uploaded documents."
)

RAG_SYSTEM_PROMPT = """You are an enterprise knowledge assistant for a single organization.

Rules:
1. Answer ONLY using the context provided in the user message. Do not use outside knowledge.
2. For multi-part questions, answer each part you can in separate paragraphs. Combine facts across sources when needed (e.g. a guide plus a resume). If one part lacks context, state specifically what is missing — never append "The information is not available in the uploaded documents." after you already answered other parts. Use that exact phrase only as the entire response when the context has nothing relevant to any part of the question.
3. Subjective or judgment questions about a person (e.g. "is X a bad/good developer?"): if the context includes their skills, experience, projects, or achievements, answer with those facts. Note that documents rarely use labels like "bad" or "good", then summarize the qualifications from the context that speak to the question.
4. Be concise, professional, and factual.
5. When you use facts from the context, cite at most one source per paragraph using (Source N) at the end of that paragraph, where N matches the source label in the context.
6. Do not invent policies, numbers, names, or dates that are not in the context."""

RAG_USER_INSTRUCTIONS = """Instructions:
- Use only the context above. Each block is labeled [Source N: filename, page, chunk_id].
- Write clear, professional prose. Prefer short paragraphs over bullet dumps unless the question asks for a list.
- Multi-part questions: address each part in its own paragraph when possible. Combine facts across sources (e.g. a resume plus a guide) when the question spans people and documents.
- Subjective or judgment questions about a person (good/bad/skilled): if skills, experience, projects, or achievements appear in the context, answer with those facts. State that documents rarely use subjective labels, then summarize relevant qualifications.
- If you can answer part of the question, answer that part and name what is still missing. Do not append a blanket "not available" line after paragraphs that already answered something.
- Use the exact phrase "The information is not available in the uploaded documents." only when the context has nothing relevant to any part of the question.
- Cite at most one source per paragraph: put (Source N) at the end of the paragraph that used that source, matching the Source label in the context.
- Do not invent numbers, names, dates, or policies. Quote figures and names exactly as they appear in the context.
- For yes/no questions, lead with a direct yes or no when the context supports it, then explain briefly with evidence."""


def answer_question(
    *,
    db: Session,
    organization_id: uuid.UUID,
    user_id: uuid.UUID,
    question: str,
    role: str,
) -> QueryResponse:
    started = time.perf_counter()
    timings: dict[str, int] = {}

    cached, cache_meta = _lookup_cached_answer(
        db,
        organization_id=organization_id,
        role=role,
        question=question,
        timings=timings,
    )
    if cached is not None:
        timings["total_ms"] = _elapsed_ms(started)
        _schedule_query_log(
            organization_id=organization_id,
            user_id=user_id,
            question=question,
            answer=cached.answer,
            latency_ms=timings["total_ms"],
            retrieved_chunk_ids=cache_meta.get("retrieved_chunk_ids", []),
            token_usage={
                "cache_hit": cache_meta.get("cache_hit", True),
                "stage_timings_ms": timings,
            },
        )
        return cached

    query_embedding = cache_meta["query_embedding"]
    hits, timings = _search_hits(
        db,
        organization_id=organization_id,
        query_embedding=query_embedding,
        question=question,
        role=role,
        timings=timings,
    )
    retrieved_chunk_ids = [str(hit.chunk_id) for hit in hits]

    if not hits:
        response = QueryResponse(answer=NO_CONTEXT_ANSWER, citations=[])
        _store_response_cache(
            organization_id=organization_id,
            role=role,
            question=question,
            response=response,
            query_embedding=query_embedding,
            retrieved_chunk_ids=retrieved_chunk_ids,
        )
        timings["total_ms"] = _elapsed_ms(started)
        _log_stage_timings(organization_id, user_id, question, timings)
        _schedule_query_log(
            organization_id=organization_id,
            user_id=user_id,
            question=question,
            answer=response.answer,
            latency_ms=timings["total_ms"],
            retrieved_chunk_ids=retrieved_chunk_ids,
            token_usage={"stage_timings_ms": timings},
        )
        return response

    llm_hits = trim_hits_for_llm(hits)
    user_prompt = _build_user_prompt(question=question, hits=llm_hits)

    t_llm = time.perf_counter()
    llm_result = get_llm_provider().complete_with_usage(
        system=_build_system_prompt(),
        user=user_prompt,
    )
    timings["llm_total_ms"] = int((time.perf_counter() - t_llm) * 1000)
    timings["llm_ttft_ms"] = timings["llm_total_ms"]

    answer = normalize_llm_answer(llm_result.text)
    citations = build_llm_source_citations(
        llm_hits,
        include=answer.strip() != NO_CONTEXT_ANSWER,
    )
    response = QueryResponse(answer=answer, citations=citations)

    _store_response_cache(
        organization_id=organization_id,
        role=role,
        question=question,
        response=response,
        query_embedding=query_embedding,
        retrieved_chunk_ids=retrieved_chunk_ids,
    )
    timings["total_ms"] = _elapsed_ms(started)
    token_usage = _merge_token_usage(llm_result.token_usage, timings)
    _log_stage_timings(organization_id, user_id, question, timings)
    _schedule_query_log(
        organization_id=organization_id,
        user_id=user_id,
        question=question,
        answer=response.answer,
        latency_ms=timings["total_ms"],
        retrieved_chunk_ids=retrieved_chunk_ids,
        token_usage=token_usage,
    )
    return response


def stream_answer_question(
    *,
    db: Session,
    organization_id: uuid.UUID,
    user_id: uuid.UUID,
    question: str,
    role: str,
) -> Iterator[str]:
    """Yield Server-Sent Events: citations → token* → done."""
    started = time.perf_counter()
    timings: dict[str, int] = {}

    cached, cache_meta = _lookup_cached_answer(
        db,
        organization_id=organization_id,
        role=role,
        question=question,
        timings=timings,
    )
    if cached is not None:
        timings["total_ms"] = _elapsed_ms(started)
        yield _sse(
            "citations",
            {
                "citations": _citations_json(cached.citations),
                "cached": True,
                "cache_hit": cache_meta.get("cache_hit"),
                "stage_timings_ms": timings,
            },
        )
        yield _sse(
            "done",
            {
                "answer": cached.answer,
                "citations": _citations_json(cached.citations),
                "cached": True,
                "cache_hit": cache_meta.get("cache_hit"),
                "latency_ms": timings["total_ms"],
                "stage_timings_ms": timings,
            },
        )
        _schedule_query_log(
            organization_id=organization_id,
            user_id=user_id,
            question=question,
            answer=cached.answer,
            latency_ms=timings["total_ms"],
            retrieved_chunk_ids=cache_meta.get("retrieved_chunk_ids", []),
            token_usage={
                "cache_hit": cache_meta.get("cache_hit", True),
                "stage_timings_ms": timings,
            },
        )
        return

    query_embedding = cache_meta["query_embedding"]
    hits, timings = _search_hits(
        db,
        organization_id=organization_id,
        query_embedding=query_embedding,
        question=question,
        role=role,
        timings=timings,
    )
    retrieved_chunk_ids = [str(hit.chunk_id) for hit in hits]

    yield _sse(
        "citations",
        {
            "citations": [],
            "stage_timings_ms": dict(timings),
        },
    )

    if not hits:
        response = QueryResponse(answer=NO_CONTEXT_ANSWER, citations=[])
        _store_response_cache(
            organization_id=organization_id,
            role=role,
            question=question,
            response=response,
            query_embedding=query_embedding,
            retrieved_chunk_ids=retrieved_chunk_ids,
        )
        timings["total_ms"] = _elapsed_ms(started)
        _log_stage_timings(organization_id, user_id, question, timings)
        yield _sse(
            "done",
            {
                "answer": NO_CONTEXT_ANSWER,
                "citations": [],
                "latency_ms": timings["total_ms"],
                "stage_timings_ms": timings,
            },
        )
        _schedule_query_log(
            organization_id=organization_id,
            user_id=user_id,
            question=question,
            answer=NO_CONTEXT_ANSWER,
            latency_ms=timings["total_ms"],
            retrieved_chunk_ids=retrieved_chunk_ids,
            token_usage={"stage_timings_ms": timings},
        )
        return

    llm_hits = trim_hits_for_llm(hits)
    user_prompt = _build_user_prompt(question=question, hits=llm_hits)

    t_llm = time.perf_counter()
    answer_parts: list[str] = []
    ttft_ms: int | None = None
    token_usage: dict[str, int] | None = None

    for part in get_llm_provider().stream_complete_with_usage(
        system=_build_system_prompt(),
        user=user_prompt,
    ):
        if isinstance(part, dict):
            token_usage = part
            continue
        if ttft_ms is None:
            ttft_ms = int((time.perf_counter() - t_llm) * 1000)
        answer_parts.append(part)
        yield _sse("token", {"text": part})

    timings["llm_ttft_ms"] = ttft_ms or 0
    timings["llm_total_ms"] = int((time.perf_counter() - t_llm) * 1000)
    timings["total_ms"] = _elapsed_ms(started)

    answer = normalize_llm_answer("".join(answer_parts))
    final_citations = build_llm_source_citations(
        llm_hits,
        include=answer != NO_CONTEXT_ANSWER,
    )
    response = QueryResponse(answer=answer, citations=final_citations)
    _store_response_cache(
        organization_id=organization_id,
        role=role,
        question=question,
        response=response,
        query_embedding=query_embedding,
        retrieved_chunk_ids=retrieved_chunk_ids,
    )
    merged_usage = _merge_token_usage(token_usage, timings)
    _log_stage_timings(organization_id, user_id, question, timings)
    yield _sse(
        "done",
        {
            "answer": answer,
            "citations": _citations_json(final_citations),
            "latency_ms": timings["total_ms"],
            "stage_timings_ms": timings,
            "token_usage": token_usage,
        },
    )
    _schedule_query_log(
        organization_id=organization_id,
        user_id=user_id,
        question=question,
        answer=answer,
        latency_ms=timings["total_ms"],
        retrieved_chunk_ids=retrieved_chunk_ids,
        token_usage=merged_usage,
    )


def _lookup_cached_answer(
    db: Session,
    *,
    organization_id: uuid.UUID,
    role: str,
    question: str,
    timings: dict[str, int],
) -> tuple[QueryResponse | None, dict]:
    exact = get_cached_answer(
        organization_id=organization_id,
        role=role,
        question=question,
    )
    if exact is not None:
        timings["cache_lookup_ms"] = 0
        return exact, {
            "cache_hit": "exact",
            "retrieved_chunk_ids": [str(c.chunk_id) for c in exact.citations],
        }

    query_embedding, timings = _get_query_embedding(question, timings)
    semantic_hit = get_semantic_cache_hit(
        organization_id=organization_id,
        role=role,
        query_embedding=query_embedding,
    )
    if semantic_hit is not None:
        if chunks_exist_for_org(
            db,
            organization_id=organization_id,
            chunk_ids=semantic_hit.retrieved_chunk_ids,
        ):
            timings["semantic_similarity"] = int(semantic_hit.similarity * 1000)
            return semantic_hit.response, {
                "cache_hit": "semantic",
                "retrieved_chunk_ids": semantic_hit.retrieved_chunk_ids,
            }

    return None, {"query_embedding": query_embedding}


def _get_query_embedding(question: str, timings: dict[str, int]) -> tuple[list[float], dict[str, int]]:
    t0 = time.perf_counter()
    query_embedding = get_cached_embedding(question)
    if query_embedding is None:
        query_embedding = get_embedding_provider().embed(question)
        set_cached_embedding(question, query_embedding)
    timings["embed_ms"] = int((time.perf_counter() - t0) * 1000)
    return query_embedding, timings


def _search_hits(
    db: Session,
    *,
    organization_id: uuid.UUID,
    query_embedding: list[float],
    question: str,
    role: str,
    timings: dict[str, int],
) -> tuple[list[ChunkSearchResult], dict[str, int]]:
    settings = get_settings()
    allowed_levels = allowed_levels_for_role(role)

    try:
        hits, search_timings = hybrid_retrieve(
            db,
            organization_id=organization_id,
            question=question,
            query_embedding=query_embedding,
            allowed_access_levels=allowed_levels,
            top_k=settings.rag_search_top_k,
        )
    except VectorIndexCorruptedError:
        logger.warning(
            "Chroma index corrupt for org %s; rebuilding from Postgres before retry",
            organization_id,
        )
        rebuild_org_vector_index(db, organization_id=organization_id)
        hits, search_timings = hybrid_retrieve(
            db,
            organization_id=organization_id,
            question=question,
            query_embedding=query_embedding,
            allowed_access_levels=allowed_levels,
            top_k=settings.rag_search_top_k,
        )
    timings.update(search_timings)

    t0 = time.perf_counter()
    hits = rerank_hits(
        question=question,
        hits=hits,
        top_n=settings.rag_search_top_k,
    )
    hits = diversify_hits_by_document(
        hits,
        top_n=settings.rag_rerank_top_n,
        min_per_document=2,
    )
    timings["rerank_ms"] = int((time.perf_counter() - t0) * 1000)

    return hits, timings


def _store_response_cache(
    *,
    organization_id: uuid.UUID,
    role: str,
    question: str,
    response: QueryResponse,
    query_embedding: list[float],
    retrieved_chunk_ids: list[str],
) -> None:
    set_cached_answer(
        organization_id=organization_id,
        role=role,
        question=question,
        response=response,
        query_embedding=query_embedding,
        retrieved_chunk_ids=retrieved_chunk_ids,
    )


def diversify_hits_by_document(
    hits: list[ChunkSearchResult],
    *,
    top_n: int,
    min_per_document: int = 2,
) -> list[ChunkSearchResult]:
    """Spread top results across documents so multi-doc questions see each upload."""
    if not hits or top_n <= 0:
        return []

    by_document: dict[uuid.UUID, list[ChunkSearchResult]] = {}
    for hit in hits:
        by_document.setdefault(hit.document_id, []).append(hit)

    if len(by_document) <= 1:
        return hits[:top_n]

    selected: list[ChunkSearchResult] = []
    selected_ids: set[uuid.UUID] = set()

    for doc_hits in by_document.values():
        for hit in doc_hits[:min_per_document]:
            if hit.chunk_id in selected_ids:
                continue
            selected.append(hit)
            selected_ids.add(hit.chunk_id)

    for hit in hits:
        if len(selected) >= top_n:
            break
        if hit.chunk_id in selected_ids:
            continue
        selected.append(hit)
        selected_ids.add(hit.chunk_id)

    return selected[:top_n]


def trim_hits_for_llm(hits: list[ChunkSearchResult]) -> list[ChunkSearchResult]:
    settings = get_settings()
    trimmed: list[ChunkSearchResult] = []
    for hit in hits[: settings.rag_llm_context_chunks]:
        content = hit.content
        if len(content) > settings.rag_chunk_max_chars:
            content = content[: settings.rag_chunk_max_chars].rstrip() + "…"
        trimmed.append(replace(hit, content=content))
    return trimmed


def _elapsed_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, default=str)}\n\n"


def _citations_json(citations: list[Citation]) -> list[dict]:
    return [c.model_dump(mode="json") for c in citations]


def _merge_token_usage(
    token_usage: dict[str, int] | None,
    timings: dict[str, int],
) -> dict:
    merged: dict = {"stage_timings_ms": timings}
    if token_usage:
        merged.update(token_usage)
    return merged


def _log_stage_timings(
    organization_id: uuid.UUID,
    user_id: uuid.UUID,
    question: str,
    timings: dict[str, int],
) -> None:
    logger.info(
        "rag_query_timings org=%s user=%s question_len=%d timings=%s",
        organization_id,
        user_id,
        len(question),
        timings,
    )


def _schedule_query_log(
    *,
    organization_id: uuid.UUID,
    user_id: uuid.UUID,
    question: str,
    answer: str,
    latency_ms: int,
    retrieved_chunk_ids: list[str],
    token_usage: dict | None,
) -> None:
    def _write() -> None:
        db = SessionLocal()
        try:
            create_query_log(
                db,
                organization_id=organization_id,
                user_id=user_id,
                question=question,
                answer=answer,
                latency_ms=latency_ms,
                retrieved_chunk_ids=retrieved_chunk_ids,
                token_usage=token_usage,
            )
            db.commit()
        except Exception:
            db.rollback()
            logger.exception("Failed to persist query log")
        finally:
            db.close()

    threading.Thread(target=_write, daemon=True).start()


def normalize_llm_answer(answer: str) -> str:
    """Drop a trailing no-context phrase when the model already gave a partial answer."""
    text = answer.strip()
    if not text or text == NO_CONTEXT_ANSWER:
        return text or NO_CONTEXT_ANSWER

    for separator in ("\n\n", "\n"):
        suffix = f"{separator}{NO_CONTEXT_ANSWER}"
        if text.endswith(suffix):
            trimmed = text[: -len(suffix)].strip()
            if len(trimmed) >= 40:
                return trimmed

    if text.endswith(NO_CONTEXT_ANSWER):
        trimmed = text[: -len(NO_CONTEXT_ANSWER)].strip()
        if len(trimmed) >= 40:
            return re.sub(r"\n{3,}", "\n\n", trimmed)

    return text


def _build_system_prompt() -> str:
    return RAG_SYSTEM_PROMPT


def _build_user_prompt(*, question: str, hits: list[ChunkSearchResult]) -> str:
    blocks: list[str] = []
    for index, hit in enumerate(hits, start=1):
        header = f"[Source {index}: {hit.filename}"
        if hit.page_number is not None:
            header += f", page {hit.page_number}"
        if hit.section_name:
            header += f", section {hit.section_name}"
        header += f", chunk_id {hit.chunk_id}"
        header += "]"
        blocks.append(f"{header}\n{hit.content}")

    context = "\n\n".join(blocks)
    return (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"{RAG_USER_INSTRUCTIONS}"
    )


def build_llm_source_citations(
    hits: list[ChunkSearchResult],
    *,
    include: bool = True,
) -> list[Citation]:
    """One citation per LLM context source, indexed to match (Source N) in the answer."""
    if not include:
        return []

    return [
        search_hit_to_citation(hit, source_index=index)
        for index, hit in enumerate(hits, start=1)
    ]


def build_citations_from_hits(
    hits: list[ChunkSearchResult],
    *,
    include: bool = True,
) -> list[Citation]:
    """Map Chroma hits to API citations (ADR-008), deduped by document + page."""
    if not include:
        return []

    citations: list[Citation] = []
    seen: set[tuple[uuid.UUID, int | None]] = set()

    for hit in hits:
        key = (hit.document_id, hit.page_number)
        if key in seen:
            continue
        seen.add(key)
        citations.append(search_hit_to_citation(hit))

    return citations


def search_hit_to_citation(
    hit: ChunkSearchResult,
    *,
    source_index: int | None = None,
) -> Citation:
    section = hit.section_name.strip() if hit.section_name else None
    return Citation(
        document=hit.filename,
        document_id=hit.document_id,
        page=hit.page_number,
        section=section or None,
        chunk_id=hit.chunk_id,
        source_index=source_index,
    )
