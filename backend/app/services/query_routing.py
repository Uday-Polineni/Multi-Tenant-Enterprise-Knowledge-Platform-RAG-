"""Lightweight query routing: filename detection and document scoping."""

from __future__ import annotations

import re
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.document import Document

_PDF_FILENAME_RE = re.compile(r"\b([\w][\w.-]*\.pdf)\b", re.IGNORECASE)
_PAGE_NUMBER_RE = re.compile(r"\bpage\s+(\d+)\b", re.IGNORECASE)
_AUDIT_TOKEN_RE = re.compile(r"\b(AUDIT-[\w-]+)\b", re.IGNORECASE)


def extract_pdf_filenames(question: str) -> list[str]:
    """Return unique PDF filenames mentioned in the question, in order of appearance."""
    seen: set[str] = set()
    filenames: list[str] = []
    for match in _PDF_FILENAME_RE.finditer(question):
        name = match.group(1)
        key = name.lower()
        if key not in seen:
            seen.add(key)
            filenames.append(name)
    return filenames


def resolve_document_filter_ids(
    db: Session,
    *,
    organization_id: uuid.UUID,
    filenames: list[str],
) -> list[uuid.UUID] | None:
    """Map mentioned filenames to document ids for the org.

    Returns None when no filenames were mentioned (search the full corpus).
    Returns a non-empty list when at least one filename resolved.
    Returns an empty list when filenames were mentioned but none matched — caller
    should fall back to unscoped search.
    """
    if not filenames:
        return None

    resolved: list[uuid.UUID] = []
    seen_ids: set[uuid.UUID] = set()
    for filename in filenames:
        document = _lookup_document_by_filename(
            db,
            organization_id=organization_id,
            filename=filename,
        )
        if document is None:
            continue
        if document.id in seen_ids:
            continue
        seen_ids.add(document.id)
        resolved.append(document.id)
    return resolved


def extract_page_number(question: str) -> int | None:
    """Return the page number when the question names one (e.g. 'page 6', 'last page (page 12)')."""
    match = _PAGE_NUMBER_RE.search(question)
    if match is None:
        return None
    return int(match.group(1))


def extract_audit_token(question: str) -> str | None:
    """Return an AUDIT-* token when the question names one."""
    match = _AUDIT_TOKEN_RE.search(question)
    if match is None:
        return None
    return match.group(1)


def should_skip_document_diversification(
    document_filter_ids: list[uuid.UUID] | None,
    *,
    page_number: int | None = None,
    topic_count: int = 0,
) -> bool:
    """Skip min-per-document spreading for scoped or multi-topic queries."""
    if page_number is not None:
        return True
    if topic_count >= 2:
        return True
    return document_filter_ids is not None and len(document_filter_ids) == 1


def prefer_hits_containing_token(
    hits: list,
    token: str,
) -> list:
    """Move chunks that contain the audit token to the front of the ranked list."""
    if not hits or not token:
        return hits
    token_lower = token.lower()
    matching = [hit for hit in hits if token_lower in hit.content.lower()]
    if not matching:
        return hits
    non_matching = [hit for hit in hits if token_lower not in hit.content.lower()]
    return matching + non_matching


def _lookup_document_by_filename(
    db: Session,
    *,
    organization_id: uuid.UUID,
    filename: str,
) -> Document | None:
    exact = db.scalars(
        select(Document)
        .where(
            Document.organization_id == organization_id,
            Document.filename == filename,
        )
        .order_by(Document.created_at.desc())
        .limit(1)
    ).first()
    if exact is not None:
        return exact

    return db.scalars(
        select(Document)
        .where(
            Document.organization_id == organization_id,
            func.lower(Document.filename) == filename.lower(),
        )
        .order_by(Document.created_at.desc())
        .limit(1)
    ).first()
