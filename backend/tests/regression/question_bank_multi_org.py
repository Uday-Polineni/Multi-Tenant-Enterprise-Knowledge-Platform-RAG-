"""100 grounded questions across 3 organizations × 15 topics."""

from __future__ import annotations

from dataclasses import dataclass

from tests.regression.corpus_multi_org import (
    ORGANIZATIONS,
    TOPICS,
    TopicDocument,
    all_documents,
)


@dataclass(frozen=True)
class MultiOrgQuestion:
    id: str
    org_code: str
    org_name: str
    question: str
    expect_any: tuple[str, ...]
    source_file: str
    source_page: int
    ground_truth: str
    question_type: str  # primary | page_fact | late_page


def _document(org_code: str, topic_slug: str) -> TopicDocument:
    for document in all_documents():
        if document.org.code == org_code and document.topic.slug == topic_slug:
            return document
    raise KeyError(f"document not found: {org_code}/{topic_slug}")


def build_multi_org_question_bank() -> list[MultiOrgQuestion]:
    questions: list[MultiOrgQuestion] = []

    # 45 primary — one per document (15 topics × 3 orgs)
    for org in ORGANIZATIONS:
        for topic in TOPICS:
            document = _document(org.code, topic.slug)
            primary = document.primary_line()
            value = topic.primary_value(org)
            qid = f"{org.code}_{topic.slug}_primary"
            questions.append(
                MultiOrgQuestion(
                    id=qid,
                    org_code=org.code,
                    org_name=org.name,
                    question=(
                        f"According to {document.filename}, what is the {topic.primary_question} "
                        f"for {org.name}?"
                    ),
                    expect_any=(value,),
                    source_file=document.filename,
                    source_page=1,
                    ground_truth=primary,
                    question_type="primary",
                )
            )

    # 45 page-fact — mid-page audit token per document
    for org in ORGANIZATIONS:
        for topic in TOPICS:
            document = _document(org.code, topic.slug)
            page = max(2, document.page_count // 2)
            fact = document.fact_for_page(page)
            qid = f"{org.code}_{topic.slug}_p{page:02d}"
            questions.append(
                MultiOrgQuestion(
                    id=qid,
                    org_code=org.code,
                    org_name=org.name,
                    question=(
                        f"In {document.filename}, what value is recorded for audit token "
                        f"{fact.audit_token} on page {page}?"
                    ),
                    expect_any=(fact.audit_token, str(fact.audit_value)),
                    source_file=document.filename,
                    source_page=page,
                    ground_truth=fact.canonical_line,
                    question_type="page_fact",
                )
            )

    # 10 late-page — last page of first 10 topic slugs for Acme only
    for topic in TOPICS[:10]:
        document = _document("acme", topic.slug)
        page = document.page_count
        fact = document.fact_for_page(page)
        qid = f"acme_{topic.slug}_plast"
        questions.append(
            MultiOrgQuestion(
                id=qid,
                org_code="acme",
                org_name="Acme Corporation",
                question=(
                    f"According to {document.filename}, what is the audit value on the last page "
                    f"(page {page}) for token {fact.audit_token}?"
                ),
                expect_any=(str(fact.audit_value), fact.audit_token),
                source_file=document.filename,
                source_page=page,
                ground_truth=fact.canonical_line,
                question_type="late_page",
            )
        )

    if len(questions) != 100:
        raise RuntimeError(f"Expected 100 questions, got {len(questions)}")
    return questions


MULTI_ORG_QUESTIONS = build_multi_org_question_bank()
