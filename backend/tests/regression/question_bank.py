"""Question bank with expected signals for regression scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegressionQuestion:
    id: str
    question: str
    expect_any: tuple[str, ...] = ()  # at least one must appear (case-insensitive)
    expect_none: tuple[str, ...] = ()  # must not appear
    expect_refusal: bool = False  # answer should be a not-available refusal
    category: str = "rag"
    notes: str = ""


RAG_QUESTIONS: list[RegressionQuestion] = [
    RegressionQuestion("pto_unique", "How many PTO days do employees get?", ("18",), (), "hr", "Unique HR doc"),
    RegressionQuestion("pto_short", "What is the PTO allowance in the short vacation document?", ("18",), (), "size_variant"),
    RegressionQuestion("pto_long", "How many annual PTO days in the long hr vacation variant?", ("18",), (), "size_variant"),
    RegressionQuestion("parental", "How long is parental leave?", ("12",), (), "hr"),
    RegressionQuestion("meal", "What is the daily meal reimbursement limit?", ("75",), (), "finance"),
    RegressionQuestion("travel", "When does travel need VP approval?", ("2000",), (), "finance"),
    RegressionQuestion("oncall", "What tool is used for on-call rotation?", ("pagerduty",), (), "engineering"),
    RegressionQuestion("deploy", "Which days are production deploys allowed?", ("tuesday", "thursday"), (), "engineering"),
    RegressionQuestion("password", "Minimum password length?", ("14",), (), "security"),
    RegressionQuestion("mfa", "Is MFA required for VPN?", ("mfa", "required"), (), "security"),
    RegressionQuestion("quota", "What is the Q1 sales quota?", ("1.2",), (), "sales"),
    RegressionQuestion("nda", "How long is the standard NDA term?", ("5",), (), "legal"),
    RegressionQuestion("datacenter", "Where is the primary datacenter?", ("dallas",), (), "ops"),
    RegressionQuestion("feature_x", "When does Feature X ship?", ("q3", "2026"), (), "product"),
    RegressionQuestion("p1_sla", "What is the P1 support SLA response time?", ("4",), (), "support"),
    RegressionQuestion("brand", "What is the brand primary color?", ("2563eb",), (), "marketing"),
    RegressionQuestion("intern", "How long is the internship program?", ("12",), (), "intern"),
    RegressionQuestion("alex_skills", "What skills does Alex Chen have?", ("python", "fastapi"), (), "person"),
    RegressionQuestion("jordan_skills", "What does Jordan Lee specialize in?", ("spark", "airflow"), (), "person"),
    RegressionQuestion("portfolio_weekend", "How long to finish portfolio v1?", ("weekend",), (), "portfolio"),
    RegressionQuestion("alex_bad_dev", "Is Alex Chen a bad developer?", ("alex",), ("not available in the uploaded documents",), "judgment", "Should use resume facts"),
    RegressionQuestion("morgan_judgment", "Is Morgan Taylor an experienced QA lead?", ("morgan",), (), "judgment"),
    RegressionQuestion("multi_cross", "What is Project Falcon budget and timeline?", ("250000", "6 months"), (), "multi_doc"),
    RegressionQuestion("duplicate_pto", "How many PTO days according to duplicate vacation files?", ("18",), (), "duplicate"),
    RegressionQuestion(
        "no_context",
        "What is the capital of Mars Colony Seven?",
        expect_refusal=True,
        category="negative",
    ),
    RegressionQuestion("rag_acronym", "What does RAG mean in internal docs?", ("retrieval augmented",), (), "engineering"),
    RegressionQuestion("remote_work", "How many days per week can employees work from home?", ("3",), (), "hr"),
    RegressionQuestion("retention", "How long are customer logs retained?", ("90",), (), "security"),
    RegressionQuestion("bonus", "What percent is the bonus pool?", ("12.5",), (), "finance"),
    RegressionQuestion("fiscal", "When does the fiscal year end?", ("march 31",), (), "finance"),
]

SURFACE_CHECKS: list[tuple[str, str]] = [
    ("health", "GET /health"),
    ("auth_register", "POST /api/v1/auth/register"),
    ("auth_login", "POST /api/v1/auth/login"),
    ("documents_list", "GET /api/v1/documents"),
    ("documents_upload", "POST /api/v1/documents/upload"),
    ("documents_get", "GET /api/v1/documents/{id}"),
    ("documents_delete", "DELETE /api/v1/documents/{id}"),
    ("query_stream", "POST /api/v1/query/stream"),
    ("analytics", "GET /api/v1/analytics/queries"),
]
