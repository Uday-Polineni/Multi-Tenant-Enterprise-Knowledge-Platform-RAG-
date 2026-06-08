"""Ten large PDF handbooks (200–300 pages) with per-page ground-truth facts."""

from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

import fitz

FILLER = (
    "This section provides supplemental operational guidance for enterprise teams. "
    "Teams should reference the KEY_FACT line at the top of each page during audits. "
    "Supporting notes cover compliance, training, approvals, and cross-functional handoffs. "
)


@dataclass(frozen=True)
class PageFact:
    page: int
    doc_slug: str
    filename: str
    cert_id: str
    score: int
    canonical_line: str

    @property
    def validation_terms(self) -> tuple[str, ...]:
        return (self.cert_id, str(self.score), f"page {self.page}")


@dataclass(frozen=True)
class LargeDocument:
    slug: str
    filename: str
    domain: str
    page_count: int

    def fact_for_page(self, page: int) -> PageFact:
        score = page * 7
        cert_id = f"CERT-{self.slug}-{page:04d}"
        line = (
            f"KEY_FACT PAGE {page}: In {self.filename} ({self.domain}), "
            f"certification {cert_id} has score {score} points and status ACTIVE."
        )
        return PageFact(
            page=page,
            doc_slug=self.slug,
            filename=self.filename,
            cert_id=cert_id,
            score=score,
            canonical_line=line,
        )

    def page_text(self, page: int) -> str:
        fact = self.fact_for_page(page)
        repeats = 12 if self.page_count >= 200 else 6
        body = FILLER * repeats
        return f"{fact.canonical_line}\n\n{body}"


LARGE_DOCUMENTS: tuple[LargeDocument, ...] = (
    LargeDocument("hr", "large_hr_handbook.pdf", "Human Resources", 250),
    LargeDocument("fin", "large_finance_policy.pdf", "Finance", 260),
    LargeDocument("eng", "large_engineering_wiki.pdf", "Engineering", 240),
    LargeDocument("sec", "large_security_manual.pdf", "Security", 275),
    LargeDocument("ops", "large_operations_guide.pdf", "Operations", 220),
    LargeDocument("sale", "large_sales_playbook.pdf", "Sales", 285),
    LargeDocument("leg", "large_legal_compendium.pdf", "Legal", 230),
    LargeDocument("mkt", "large_marketing_brand_book.pdf", "Marketing", 255),
    LargeDocument("sup", "large_support_runbook.pdf", "Support", 245),
    LargeDocument("pro", "large_product_specs.pdf", "Product", 300),
)


def sample_question_pages(page_count: int, questions_per_doc: int = 10) -> list[int]:
    """Spread questions across early, middle, and late pages."""
    if questions_per_doc <= 0:
        return []
    step = max(1, (page_count - 20) // questions_per_doc)
    pages = []
    for index in range(questions_per_doc):
        page = min(page_count - 5, 10 + index * step)
        if page not in pages:
            pages.append(page)
    while len(pages) < questions_per_doc:
        candidate = min(page_count - 5, pages[-1] + 3 if pages else 10)
        if candidate not in pages:
            pages.append(candidate)
        else:
            break
    return pages[:questions_per_doc]


def build_ground_truth_index() -> dict[str, PageFact]:
    index: dict[str, PageFact] = {}
    for document in LARGE_DOCUMENTS:
        for page in range(1, document.page_count + 1):
            fact = document.fact_for_page(page)
            index[f"{document.slug}:{page}"] = fact
    return index


def render_large_pdf(document: LargeDocument) -> bytes:
    pdf = fitz.open()
    for page_num in range(1, document.page_count + 1):
        page = pdf.new_page(width=612, height=792)
        text = document.page_text(page_num)
        rect = fitz.Rect(50, 50, 562, 742)
        page.insert_textbox(rect, text, fontsize=9, fontname="helv")
    buffer = io.BytesIO()
    pdf.save(buffer, garbage=4, deflate=True)
    pdf.close()
    return buffer.getvalue()


def write_large_corpus(target_dir: Path, *, documents: tuple[LargeDocument, ...] | None = None) -> list[Path]:
    target_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for document in documents or LARGE_DOCUMENTS:
        path = target_dir / document.filename
        path.write_bytes(render_large_pdf(document))
        paths.append(path)
    return paths


def verify_fact_in_pdf(pdf_path: Path, fact: PageFact) -> bool:
    doc = fitz.open(pdf_path)
    try:
        if fact.page < 1 or fact.page > doc.page_count:
            return False
        text = doc.load_page(fact.page - 1).get_text()
        return fact.cert_id in text and str(fact.score) in text
    finally:
        doc.close()
