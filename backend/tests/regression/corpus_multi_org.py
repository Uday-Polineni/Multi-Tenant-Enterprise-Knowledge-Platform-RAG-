"""15-topic, 10–15 page PDFs for 3 organizations with embedded ground-truth facts."""

from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

import fitz

FILLER = (
    "Operational guidance for enterprise knowledge teams. "
    "Reference the KEY_FACT line on each page during compliance reviews. "
    "This filler text increases page length without changing audit values. "
)


@dataclass(frozen=True)
class OrganizationSpec:
    code: str
    name: str
    value_index: int  # index into per-topic value lists


@dataclass(frozen=True)
class TopicSpec:
    slug: str
    label: str
    primary_question: str
    primary_template: str  # contains {v}
    values: tuple[str, str, str]  # acme, beta, gamma

    def page_count(self) -> int:
        base = sum(ord(ch) for ch in self.slug)
        return 10 + (base % 6)  # 10–15 pages

    def primary_value(self, org: OrganizationSpec) -> str:
        return self.values[org.value_index]

    def primary_line(self, org: OrganizationSpec) -> str:
        return (
            f"KEY_FACT: [{org.code.upper()}] {self.label} — "
            f"{self.primary_template.format(v=self.primary_value(org))}"
        )


@dataclass(frozen=True)
class PageFact:
    org_code: str
    topic_slug: str
    filename: str
    page: int
    audit_token: str
    audit_value: int
    canonical_line: str

    @property
    def validation_terms(self) -> tuple[str, ...]:
        return (self.audit_token, str(self.audit_value))


@dataclass(frozen=True)
class TopicDocument:
    org: OrganizationSpec
    topic: TopicSpec

    @property
    def filename(self) -> str:
        return f"{self.org.code}_{self.topic.slug}.pdf"

    @property
    def page_count(self) -> int:
        return self.topic.page_count()

    def primary_line(self) -> str:
        return self.topic.primary_line(self.org)

    def page_text(self, page: int) -> str:
        if page == 1:
            header = self.primary_line()
        else:
            fact = self.fact_for_page(page)
            header = fact.canonical_line
        body = FILLER * 8
        return f"{header}\n\nTopic: {self.topic.label}\nOrganization: {self.org.name}\n\n{body}"

    def fact_for_page(self, page: int) -> PageFact:
        multiplier = 10 + self.org.value_index * 3
        audit_value = page * multiplier
        token = f"AUDIT-{self.org.code.upper()}-{self.topic.slug.upper()}-{page:02d}"
        line = (
            f"KEY_FACT PAGE {page}: [{self.org.code.upper()}] {self.topic.label} "
            f"audit token {token} records value {audit_value}."
        )
        return PageFact(
            org_code=self.org.code,
            topic_slug=self.topic.slug,
            filename=self.filename,
            page=page,
            audit_token=token,
            audit_value=audit_value,
            canonical_line=line,
        )


ORGANIZATIONS: tuple[OrganizationSpec, ...] = (
    OrganizationSpec("acme", "Acme Corporation", 0),
    OrganizationSpec("beta", "Beta Industries", 1),
    OrganizationSpec("gamma", "Gamma Solutions", 2),
)

TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec("hr_vacation", "HR Vacation Policy", "annual PTO allowance", "annual PTO allowance is {v} days", ("18", "22", "15")),
    TopicSpec("finance_meals", "Finance Meal Policy", "daily meal reimbursement limit", "meal reimbursement limit is {v} dollars per day", ("75", "60", "90")),
    TopicSpec("eng_deploy", "Engineering Deploy Policy", "allowed production deploy days", "production deploys are allowed on {v} only", ("Tuesday through Thursday", "Monday through Wednesday", "Wednesday through Friday")),
    TopicSpec("security_mfa", "Security MFA Policy", "MFA requirement", "MFA is required for {v}", ("all VPN connections", "all admin consoles", "all cloud dashboards")),
    TopicSpec("sales_quota", "Sales Quota Policy", "Q1 sales quota", "Q1 sales quota is {v} million dollars", ("1.2", "0.9", "1.5")),
    TopicSpec("legal_nda", "Legal NDA Policy", "standard NDA term", "standard NDA term is {v} years", ("5", "3", "7")),
    TopicSpec("ops_datacenter", "Operations Datacenter Policy", "primary datacenter city", "primary datacenter is located in {v}", ("Dallas Texas", "Chicago Illinois", "Austin Texas")),
    TopicSpec("marketing_brand", "Marketing Brand Policy", "brand primary color hex", "brand primary color is hex {v}", ("2563eb", "dc2626", "059669")),
    TopicSpec("support_sla", "Support SLA Policy", "P1 first response SLA", "P1 support SLA is {v} hour first response", ("4", "2", "6")),
    TopicSpec("product_roadmap", "Product Roadmap Policy", "Feature X ship target", "Feature X ships in {v}", ("Q3 2026", "Q2 2026", "Q4 2026")),
    TopicSpec("compliance_retention", "Compliance Retention Policy", "customer log retention", "customer log retention is {v} days", ("90", "120", "60")),
    TopicSpec("training_budget", "Training Budget Policy", "annual training budget per engineer", "training budget is {v} dollars per engineer per year", ("1500", "2000", "1200")),
    TopicSpec("it_laptop", "IT Laptop Policy", "laptop refresh cycle", "laptop refresh cycle is {v} years", ("3", "4", "2")),
    TopicSpec("procurement_approval", "Procurement Approval Policy", "purchase approval threshold", "purchases over {v} dollars require director approval", ("5000", "3000", "7500")),
    TopicSpec("cs_onboarding", "Customer Success Onboarding Policy", "customer onboarding duration", "customer onboarding duration is {v} days", ("30", "45", "21")),
)


def all_documents() -> list[TopicDocument]:
    return [
        TopicDocument(org=org, topic=topic)
        for org in ORGANIZATIONS
        for topic in TOPICS
    ]


def render_document_pdf(document: TopicDocument) -> bytes:
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


def write_org_corpus(target_dir: Path) -> dict[str, list[Path]]:
    target_dir.mkdir(parents=True, exist_ok=True)
    paths_by_org: dict[str, list[Path]] = {org.code: [] for org in ORGANIZATIONS}
    for document in all_documents():
        org_dir = target_dir / document.org.code
        org_dir.mkdir(parents=True, exist_ok=True)
        path = org_dir / document.filename
        path.write_bytes(render_document_pdf(document))
        paths_by_org[document.org.code].append(path)
    return paths_by_org


def verify_primary_in_pdf(pdf_path: Path, *, primary_line: str) -> bool:
    doc = fitz.open(pdf_path)
    try:
        text = doc.load_page(0).get_text()
        return primary_line[:60] in text or primary_line in text
    finally:
        doc.close()


def verify_fact_in_pdf(pdf_path: Path, fact: PageFact) -> bool:
    doc = fitz.open(pdf_path)
    try:
        if fact.page < 1 or fact.page > doc.page_count:
            return False
        text = doc.load_page(fact.page - 1).get_text()
        return fact.audit_token in text and str(fact.audit_value) in text
    finally:
        doc.close()
