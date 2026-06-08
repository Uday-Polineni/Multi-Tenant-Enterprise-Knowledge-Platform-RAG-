"""Validate multi-org assistant answers against PDF ground truth."""

from __future__ import annotations

from pathlib import Path

from tests.regression.corpus_multi_org import ORGANIZATIONS, TOPICS, TopicDocument, verify_fact_in_pdf, verify_primary_in_pdf
from tests.regression.question_bank_multi_org import MultiOrgQuestion


def _document_for(item: MultiOrgQuestion) -> TopicDocument:
    for org in ORGANIZATIONS:
        if org.code != item.org_code:
            continue
        for topic in TOPICS:
            if item.source_file == f"{org.code}_{topic.slug}.pdf":
                return TopicDocument(org=org, topic=topic)
    raise KeyError(item.source_file)


def validate_multi_org_answer(
    answer: str,
    *,
    item: MultiOrgQuestion,
    pdf_path: Path | None = None,
) -> tuple[bool, str, bool]:
    if not answer or not answer.strip():
        return False, "empty answer", False

    lower = answer.lower()
    matched = [term for term in item.expect_any if term.lower() in lower]
    if not matched:
        return (
            False,
            f"answer missing ground-truth terms {item.expect_any}",
            False,
        )

    pdf_ok = False
    if pdf_path is not None and pdf_path.exists():
        if item.question_type == "primary":
            pdf_ok = verify_primary_in_pdf(pdf_path, primary_line=item.ground_truth)
        else:
            document = _document_for(item)
            fact = document.fact_for_page(item.source_page)
            pdf_ok = verify_fact_in_pdf(pdf_path, fact)

    detail = f"matched {matched}; type={item.question_type}"
    if pdf_path is not None:
        detail += f"; pdf_verified={pdf_ok}"
    return True, detail, pdf_ok
