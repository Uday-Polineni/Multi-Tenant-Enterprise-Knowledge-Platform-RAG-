"""Validate assistant answers against canonical PDF ground truth."""

from __future__ import annotations

from pathlib import Path

from tests.regression.corpus_large import PageFact, verify_fact_in_pdf


def validate_answer_against_fact(
    answer: str,
    *,
    fact: PageFact,
    expect_any: tuple[str, ...],
    pdf_path: Path | None = None,
) -> tuple[bool, str, bool]:
    """
    Returns (passed, detail, pdf_source_verified).
    Primary check: answer contains expected terms from original PDF fact.
    Secondary: fact string exists on the cited PDF page on disk.
    """
    if not answer or not answer.strip():
        return False, "empty answer", False

    lower = answer.lower()
    matched = [term for term in expect_any if term.lower() in lower]
    if not matched:
        return (
            False,
            f"answer missing ground-truth terms {expect_any}; expected score {fact.score} for {fact.cert_id}",
            False,
        )

    pdf_ok = False
    if pdf_path is not None and pdf_path.exists():
        pdf_ok = verify_fact_in_pdf(pdf_path, fact)

    detail = f"matched {matched}; ground_truth={fact.canonical_line[:120]}..."
    if pdf_path is not None:
        detail += f"; pdf_page_verified={pdf_ok}"
    return True, detail, pdf_ok
