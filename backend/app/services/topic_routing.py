"""Map natural-language employee questions to policy topic documents."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.document import Document

# (topic_slug, keywords longest-first within each topic via sort at runtime)
TOPIC_KEYWORD_ROUTES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "hr_vacation",
        (
            "paid time off",
            "time off",
            "pto allowance",
            "pto days",
            "annual pto",
            "vacation days",
            "vacation day",
            "pto",
            "vacation",
        ),
    ),
    (
        "finance_meals",
        (
            "meal reimbursement",
            "daily meal",
            "per diem",
            "meal allowance",
            "meal limit",
            "meals",
            "meal",
        ),
    ),
    (
        "eng_deploy",
        (
            "production deploy",
            "production release",
            "deploy days",
            "deployment",
            "deploys",
            "deploy",
        ),
    ),
    (
        "security_mfa",
        (
            "multi-factor authentication",
            "multifactor authentication",
            "two-factor",
            "multi-factor",
            "multifactor",
            "mfa",
            "2fa",
        ),
    ),
    (
        "sales_quota",
        (
            "q1 sales quota",
            "sales quota",
            "quota target",
            "quota",
        ),
    ),
    (
        "legal_nda",
        (
            "non-disclosure",
            "non disclosure",
            "nda term",
            "nda",
        ),
    ),
    (
        "ops_datacenter",
        (
            "data center",
            "datacenter",
            "data centre",
        ),
    ),
    (
        "marketing_brand",
        (
            "brand primary color",
            "brand color",
            "brand colour",
            "hex code",
            "hex",
        ),
    ),
    (
        "support_sla",
        (
            "first-response",
            "first response",
            "p1 support",
            "support sla",
            "support ticket",
            "p1",
            "sla",
        ),
    ),
    (
        "product_roadmap",
        (
            "feature x",
            "ship target",
            "ship date",
            "roadmap",
        ),
    ),
    (
        "compliance_retention",
        (
            "log retention",
            "customer log",
            "customer logs",
            "retain logs",
            "retention",
        ),
    ),
    (
        "training_budget",
        (
            "training budget",
            "annual training",
            "upskilling",
            "training per engineer",
        ),
    ),
    (
        "it_laptop",
        (
            "laptop refresh",
            "workstation",
            "laptop",
        ),
    ),
    (
        "procurement_approval",
        (
            "purchase approval",
            "director approval",
            "procurement",
            "purchasing",
            "purchase amount",
            "purchase threshold",
        ),
    ),
    (
        "cs_onboarding",
        (
            "customer onboarding",
            "client onboarding",
            "onboarding duration",
            "onboarding",
        ),
    ),
)

TOPIC_FOCUSED_QUERIES: dict[str, str] = {
    "hr_vacation": "What is the annual PTO or vacation day allowance for employees?",
    "finance_meals": "What is the daily meal reimbursement limit for work travel?",
    "eng_deploy": "Which days are production deploys allowed?",
    "security_mfa": "What systems or access require MFA?",
    "sales_quota": "What is the Q1 sales quota target?",
    "legal_nda": "What is the standard NDA term in years?",
    "ops_datacenter": "Where is the primary datacenter located?",
    "marketing_brand": "What is the brand primary color hex code?",
    "support_sla": "What is the P1 first-response support SLA?",
    "product_roadmap": "When is Feature X scheduled to ship?",
    "compliance_retention": "How long are customer logs retained?",
    "training_budget": "What is the annual training budget per engineer?",
    "it_laptop": "What is the laptop refresh cycle in years?",
    "procurement_approval": "Above what purchase amount is director approval required?",
    "cs_onboarding": "How many days does customer onboarding take?",
}

_SORTED_KEYWORD_ROUTES: list[tuple[str, str]] = sorted(
    (
        (keyword, slug)
        for slug, keywords in TOPIC_KEYWORD_ROUTES
        for keyword in keywords
    ),
    key=lambda item: len(item[0]),
    reverse=True,
)


def detect_topic_slugs(question: str) -> list[str]:
    """Return topic slugs matched in the question, in order of first appearance."""
    lower = question.lower()
    matches: list[tuple[int, str]] = []
    matched_spans: list[tuple[int, int]] = []

    for keyword, slug in _SORTED_KEYWORD_ROUTES:
        start = 0
        while True:
            index = lower.find(keyword, start)
            if index < 0:
                break
            end = index + len(keyword)
            overlaps = any(
                not (end <= span_start or index >= span_end)
                for span_start, span_end in matched_spans
            )
            if not overlaps:
                matched_spans.append((index, end))
                matches.append((index, slug))
            start = index + 1

    seen: set[str] = set()
    ordered: list[str] = []
    for _, slug in sorted(matches, key=lambda item: item[0]):
        if slug in seen:
            continue
        seen.add(slug)
        ordered.append(slug)
    return ordered


def resolve_document_ids_for_topic_slugs(
    db: Session,
    *,
    organization_id: uuid.UUID,
    topic_slugs: list[str],
) -> list[uuid.UUID]:
    if not topic_slugs:
        return []

    resolved: list[uuid.UUID] = []
    seen: set[uuid.UUID] = set()
    for slug in topic_slugs:
        suffix = f"_{slug}.pdf".lower()
        document = db.scalars(
            select(Document)
            .where(
                Document.organization_id == organization_id,
                func.lower(Document.filename).like(f"%{suffix}"),
            )
            .order_by(Document.created_at.desc())
            .limit(1)
        ).first()
        if document is None or document.id in seen:
            continue
        seen.add(document.id)
        resolved.append(document.id)
    return resolved
