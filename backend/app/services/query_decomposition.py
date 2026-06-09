"""Break compound employee questions into focused retrieval sub-queries."""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass

from app.services.topic_routing import TOPIC_FOCUSED_QUERIES, detect_topic_slugs

_CONJUNCTION_SPLIT_RE = re.compile(
    r"\s+and\s+(?=(?:what|which|where|when|how|who|is|are|above|at|how\s+many|how\s+long)\b)",
    re.IGNORECASE,
)
_QUESTION_CLAUSE_SPLIT_RE = re.compile(r"\?\s+")
_MIN_SUBQUERY_CHARS = 12


@dataclass(frozen=True)
class SearchQuery:
    text: str
    topic_slug: str | None = None


def build_search_queries(question: str) -> list[SearchQuery]:
    """Produce one or more retrieval queries for a user question."""
    topic_slugs = detect_topic_slugs(question)
    if len(topic_slugs) >= 2:
        return [
            SearchQuery(text=TOPIC_FOCUSED_QUERIES[slug], topic_slug=slug)
            for slug in topic_slugs
            if slug in TOPIC_FOCUSED_QUERIES
        ]

    clause_parts = _split_question_clauses(question)
    if len(clause_parts) >= 2:
        return [SearchQuery(text=part) for part in clause_parts]

    if len(topic_slugs) == 1:
        slug = topic_slugs[0]
        focused = TOPIC_FOCUSED_QUERIES.get(slug)
        if focused and focused.lower() != question.strip().lower():
            return [
                SearchQuery(text=question, topic_slug=slug),
                SearchQuery(text=focused, topic_slug=slug),
            ]
        return [SearchQuery(text=question, topic_slug=slug)]

    return [SearchQuery(text=question)]


def estimate_question_parts(search_queries: list[SearchQuery], question: str) -> int:
    """How many distinct sub-questions the user asked."""
    topic_slugs = detect_topic_slugs(question)
    if len(topic_slugs) >= 2:
        return len(topic_slugs)
    if len(search_queries) >= 2:
        return len(search_queries)
    if _looks_multi_part(question):
        return max(2, question.lower().count(" and ") + 1)
    return 1


def resolve_subquery_document_ids(
    *,
    topic_slug: str | None,
    topic_slug_to_document_id: dict[str, uuid.UUID],
    global_document_ids: list[uuid.UUID] | None,
) -> list[uuid.UUID] | None:
    if topic_slug and topic_slug in topic_slug_to_document_id:
        return [topic_slug_to_document_id[topic_slug]]
    return global_document_ids


def merge_ranked_hit_lists(
    hit_lists: list[list],
    *,
    top_n: int,
) -> list:
    if not hit_lists:
        return []
    if len(hit_lists) == 1:
        return hit_lists[0][:top_n]

    by_id: dict[uuid.UUID, object] = {}
    scores: dict[uuid.UUID, float] = {}
    for hit_list in hit_lists:
        for rank, hit in enumerate(hit_list, start=1):
            by_id[hit.chunk_id] = hit
            scores[hit.chunk_id] = scores.get(hit.chunk_id, 0.0) + 1.0 / rank

    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [by_id[chunk_id] for chunk_id, _ in ordered[:top_n]]


def _split_question_clauses(question: str) -> list[str]:
    text = question.strip()
    if not text:
        return []

    parts: list[str] = []
    for segment in _QUESTION_CLAUSE_SPLIT_RE.split(text):
        segment = segment.strip()
        if not segment:
            continue
        if not segment.endswith("?"):
            segment = f"{segment}?"
        for piece in _CONJUNCTION_SPLIT_RE.split(segment):
            piece = piece.strip()
            if not piece:
                continue
            if not piece.endswith("?"):
                piece = f"{piece}?"
            if len(piece) >= _MIN_SUBQUERY_CHARS:
                parts.append(piece)

    deduped: list[str] = []
    seen: set[str] = set()
    for part in parts:
        key = part.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(part)
    return deduped


def _looks_multi_part(question: str) -> bool:
    lower = question.lower()
    if _CONJUNCTION_SPLIT_RE.search(question):
        return True
    if lower.count("?") >= 2:
        return True
    return " and " in lower and any(
        token in lower
        for token in ("what ", "which ", "where ", "when ", "how ", "who ")
    )
