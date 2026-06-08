"""Synthetic PDF corpus for RAG regression (50 documents, varied size and topic)."""

from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

import fitz  # pymupdf

PADDING = (
    "Additional background material for chunking and retrieval tests. "
    "This padding increases document size without changing the key fact. "
    "Enterprise knowledge systems must handle short memos and long handbooks alike. "
)


@dataclass(frozen=True)
class CorpusDocument:
    filename: str
    key_fact: str
    topic: str
    size_tier: str  # short | medium | long | unique
    body: str

    def full_text(self) -> str:
        return f"{self.key_fact}\n\n{self.body}"


def _pad_to_words(base: str, target_words: int) -> str:
    words = base.split()
    chunks = [base]
    while sum(len(c.split()) for c in chunks) < target_words:
        chunks.append(PADDING)
    return "\n\n".join(chunks)


def _build_unique_docs() -> list[CorpusDocument]:
    specs = [
        ("hr_vacation_policy.pdf", "KEY_FACT: Annual PTO allowance is 18 days per employee.", "hr", "unique"),
        ("hr_parental_leave.pdf", "KEY_FACT: Parental leave is 12 weeks paid for primary caregivers.", "hr", "unique"),
        ("finance_meal_limit.pdf", "KEY_FACT: Meal reimbursement limit is 75 dollars per day.", "finance", "unique"),
        ("finance_travel_approval.pdf", "KEY_FACT: Travel over 2000 dollars requires VP pre-approval.", "finance", "unique"),
        ("eng_oncall_rotation.pdf", "KEY_FACT: On-call rotation uses PagerDuty with weekly handoffs.", "engineering", "unique"),
        ("eng_deploy_window.pdf", "KEY_FACT: Production deploys are allowed Tuesday through Thursday only.", "engineering", "unique"),
        ("security_password_policy.pdf", "KEY_FACT: Minimum password length is 14 characters.", "security", "unique"),
        ("security_mfa_vpn.pdf", "KEY_FACT: MFA is required for all VPN connections.", "security", "unique"),
        ("sales_q1_quota.pdf", "KEY_FACT: Q1 sales quota is 1.2 million dollars.", "sales", "unique"),
        ("legal_nda_term.pdf", "KEY_FACT: Standard NDA term is 5 years from signature.", "legal", "unique"),
        ("ops_primary_datacenter.pdf", "KEY_FACT: Primary datacenter is located in Dallas Texas.", "ops", "unique"),
        ("product_roadmap_feature_x.pdf", "KEY_FACT: Feature X ships in Q3 2026.", "product", "unique"),
        ("support_p1_sla.pdf", "KEY_FACT: P1 support SLA is 4 hour first response.", "support", "unique"),
        ("marketing_brand_color.pdf", "KEY_FACT: Brand primary color is hex 2563eb.", "marketing", "unique"),
        ("intern_program_length.pdf", "KEY_FACT: Internship program duration is 12 weeks.", "intern", "unique"),
    ]
    docs: list[CorpusDocument] = []
    for filename, key_fact, topic, tier in specs:
        body = _pad_to_words(
            f"Policy document {filename}. This section describes operational details for {topic} teams.",
            280,
        )
        docs.append(CorpusDocument(filename, key_fact, topic, tier, body))
    return docs


def _build_size_variant_docs() -> list[CorpusDocument]:
    variants = [
        ("hr_vacation", "KEY_FACT: Annual PTO allowance is 18 days per employee.", "hr"),
        ("finance_meal", "KEY_FACT: Meal reimbursement limit is 75 dollars per day.", "finance"),
        ("eng_oncall", "KEY_FACT: On-call rotation uses PagerDuty with weekly handoffs.", "engineering"),
        ("security_mfa", "KEY_FACT: MFA is required for all VPN connections.", "security"),
        ("product_roadmap", "KEY_FACT: Feature X ships in Q3 2026.", "product"),
    ]
    tiers = [("short", 120), ("medium", 600), ("long", 1800)]
    docs: list[CorpusDocument] = []
    for slug, key_fact, topic in variants:
        for tier_name, word_target in tiers:
            filename = f"{slug}_{tier_name}.pdf"
            body = _pad_to_words(f"Size variant {tier_name} for {slug}.", word_target)
            docs.append(CorpusDocument(filename, key_fact, topic, tier_name, body))
    return docs


def _build_edge_docs() -> list[CorpusDocument]:
    docs: list[CorpusDocument] = []
    alex_resume = (
        "KEY_FACT: Alex Chen is a Backend Software Engineer with 4 years experience in Python and FastAPI.\n\n"
        "SUMMARY\nAlex Chen builds distributed APIs and PostgreSQL-backed services.\n"
        "SKILLS\nPython, FastAPI, PostgreSQL, Redis, AWS.\n"
        "PROJECTS\nBuilt an event-driven billing pipeline processing 5000 events per minute."
    )
    jordan_resume = (
        "KEY_FACT: Jordan Lee is a Data Engineer specializing in Spark and Airflow.\n\n"
        "SUMMARY\nJordan Lee designs ETL pipelines and warehouse models.\n"
        "SKILLS\nSpark, Airflow, dbt, Snowflake, Python.\n"
        "PROJECTS\nReduced nightly ETL window from 6 hours to 90 minutes."
    )
    portfolio = (
        "KEY_FACT: Portfolio v1 can be finished in one weekend using a JSON-first React architecture.\n\n"
        "Tech stack: React, TypeScript, Vite, Tailwind CSS.\n"
        "Sections: Hero, About, Experience, Projects, Contact."
    )
    edge_specs = [
        ("person_resume_alex.pdf", alex_resume, "person", "unique"),
        ("person_resume_jordan.pdf", jordan_resume, "person", "unique"),
        ("portfolio_guide_regression.pdf", portfolio, "portfolio", "unique"),
        ("hr_vacation_duplicate_a.pdf", "KEY_FACT: Annual PTO allowance is 18 days per employee.", "hr", "short"),
        ("hr_vacation_duplicate_b.pdf", "KEY_FACT: Annual PTO allowance is 18 days per employee.", "hr", "short"),
        ("table_heavy_policy.pdf", "KEY_FACT: Tier 1 support covers 24x7 monitoring.\n\n| Tier | Hours |\n| T1 | 24x7 |\n| T2 | Business |", "support", "medium"),
        ("bullet_heavy_policy.pdf", "KEY_FACT: Remote work policy allows 3 days home per week.\n\n• Mon office\n• Tue home\n• Wed office", "hr", "medium"),
        ("long_paragraph_policy.pdf", "KEY_FACT: Data retention for customer logs is 90 days.", "security", "long"),
        ("minimal_one_liner.pdf", "KEY_FACT: Office wifi password rotates monthly.", "ops", "short"),
        ("numbers_precision.pdf", "KEY_FACT: Bonus pool allocation is 12.5 percent of net revenue.", "finance", "medium"),
        ("dates_precision.pdf", "KEY_FACT: Fiscal year ends on March 31 2027.", "finance", "medium"),
        ("acronym_glossary.pdf", "KEY_FACT: RAG means Retrieval Augmented Generation in internal docs.", "engineering", "short"),
        ("multilingual_snippet.pdf", "KEY_FACT: Welcome desk supports English and Spanish.\n\nBienvenido al portal de empleados.", "hr", "short"),
        ("cross_ref_doc_alpha.pdf", "KEY_FACT: Project Falcon budget is 250000 dollars. See companion doc Bravo for timeline.", "product", "medium"),
        ("cross_ref_doc_bravo.pdf", "KEY_FACT: Project Falcon timeline is 6 months starting January 2026.", "product", "medium"),
        ("empty_padding_1.pdf", "KEY_FACT: Parking validation is available at desk B.", "ops", "long"),
        ("empty_padding_2.pdf", "KEY_FACT: Visitor badges expire after 8 hours.", "ops", "long"),
        ("empty_padding_3.pdf", "KEY_FACT: Fire drill occurs first Wednesday monthly.", "ops", "long"),
        ("judgment_target_morgan.pdf", "KEY_FACT: Morgan Taylor is a junior QA analyst with 1 year of test automation experience.", "person", "medium"),
        ("multi_fact_dense.pdf", "KEY_FACT: Training budget is 1500 dollars per engineer per year.", "hr", "long"),
    ]
    for filename, text, topic, tier in edge_specs:
        parts = text.split("\n\n", 1)
        key_fact = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        word_targets = {"short": 100, "medium": 500, "long": 1600, "unique": 300}
        body = _pad_to_words(rest or f"Supporting content for {filename}.", word_targets.get(tier, 300))
        docs.append(CorpusDocument(filename, key_fact, topic, tier, body))
    return docs


def build_corpus() -> list[CorpusDocument]:
    docs = _build_unique_docs() + _build_size_variant_docs() + _build_edge_docs()
    if len(docs) != 50:
        raise RuntimeError(f"Expected 50 corpus documents, got {len(docs)}")
    return docs


def render_pdf_bytes(doc: CorpusDocument) -> bytes:
    text = doc.full_text()
    pdf = fitz.open()
    page = pdf.new_page(width=612, height=792)
    rect = fitz.Rect(50, 50, 562, 742)
    page.insert_textbox(rect, text, fontsize=10, fontname="helv")
    buffer = io.BytesIO()
    pdf.save(buffer)
    pdf.close()
    return buffer.getvalue()


def write_corpus_to_dir(target_dir: Path) -> list[Path]:
    target_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for doc in build_corpus():
        path = target_dir / doc.filename
        path.write_bytes(render_pdf_bytes(doc))
        paths.append(path)
    return paths
