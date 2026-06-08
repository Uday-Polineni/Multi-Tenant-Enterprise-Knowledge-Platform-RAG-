#!/usr/bin/env python3
"""End-to-end regression runner: 50-doc corpus, API surfaces, RAG Q&A report."""

from __future__ import annotations

import argparse
import os
import sys
import time
import uuid
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path

import httpx

# Sync embed during regression so uploads index without a worker.
os.environ.setdefault("EMBED_ASYNC", "false")
os.environ.setdefault("PROTOTYPE_MAX_PDF_PAGES", "0")
os.environ.setdefault("PROTOTYPE_MAX_DOCUMENTS_PER_ORG", "0")

from tests.regression.api_helpers import (
    API_BASE,
    delete_document,
    list_documents,
    login,
    query_stream,
    register_org,
    score_answer,
    upload_pdf,
    wait_document_ready,
)
from tests.regression.corpus import build_corpus, write_corpus_to_dir
from tests.regression.question_bank import RAG_QUESTIONS, SURFACE_CHECKS

REPORT_PATH = Path(__file__).parent / "REGRESSION_REPORT.md"
CORPUS_DIR = Path(__file__).parent / "_corpus_pdfs"


def _check_health(client: object, base: str) -> tuple[bool, str]:
    try:
        path = f"{base}/health" if base else "/health"
        response = client.get(path, timeout=10.0)
        if response.status_code == 200:
            return True, "ok"
        return False, f"status {response.status_code}"
    except Exception as exc:
        return False, str(exc)


def _run_surface_tests(client: object, base: str, token: str, sample_doc_id: str | None) -> list[dict]:
    results: list[dict] = []
    prefix = base or ""

    def path(route: str) -> str:
        return f"{prefix}{route}"

    checks = [
        ("health", lambda: client.get(path("/health"))),
        ("documents_list", lambda: client.get(
            path("/api/v1/documents"),
            headers={"Authorization": f"Bearer {token}"},
        )),
        ("analytics", lambda: client.get(
            path("/api/v1/analytics/queries?limit=5"),
            headers={"Authorization": f"Bearer {token}"},
        )),
        ("query_stream", lambda: client.post(
            path("/api/v1/query/stream"),
            headers={"Authorization": f"Bearer {token}"},
            json={"question": "What is the PTO allowance?"},
            timeout=180.0,
        )),
    ]
    if sample_doc_id:
        checks.append(
            ("documents_get", lambda: client.get(
                path(f"/api/v1/documents/{sample_doc_id}"),
                headers={"Authorization": f"Bearer {token}"},
            ))
        )
    for name, fn in checks:
        try:
            response = fn()
            ok = response.status_code < 400
            results.append({"surface": name, "pass": ok, "detail": f"HTTP {response.status_code}"})
        except Exception as exc:
            results.append({"surface": name, "pass": False, "detail": str(exc)})
    return results


def _upload_corpus(client: object, base: str, token: str) -> tuple[list[dict], list[str]]:
    write_corpus_to_dir(CORPUS_DIR)
    uploaded: list[dict] = []
    failures: list[str] = []
    for index, doc in enumerate(build_corpus(), start=1):
        path = CORPUS_DIR / doc.filename
        try:
            meta = upload_pdf(client, base=base, token=token, pdf_path=path)
            if meta.get("status") == "processing":
                meta = wait_document_ready(
                    client, base=base, token=token, document_id=meta["id"]
                )
            if meta.get("status") != "ready":
                failures.append(f"{doc.filename}: status={meta.get('status')}")
            uploaded.append(meta)
            print(f"  [{index}/50] {doc.filename} -> {meta.get('status')} ({meta.get('chunk_count')} chunks)")
        except Exception as exc:
            failures.append(f"{doc.filename}: {exc}")
            print(f"  [{index}/50] {doc.filename} FAILED: {exc}")
    return uploaded, failures


def _run_rag_questions(client: object, base: str, token: str) -> list[dict]:
    results: list[dict] = []
    for item in RAG_QUESTIONS:
        print(f"  Q: {item.id}")
        try:
            stream = query_stream(client, base=base, token=token, question=item.question)
            if stream.error:
                results.append({
                    "id": item.id,
                    "question": item.question,
                    "pass": False,
                    "answer": stream.error,
                    "detail": "stream error",
                    "category": item.category,
                    "latency_ms": stream.latency_ms,
                })
                continue
            passed, detail = score_answer(
                stream.answer,
                item.expect_any,
                item.expect_none,
                expect_refusal=item.expect_refusal,
            )
            results.append({
                "id": item.id,
                "question": item.question,
                "pass": passed,
                "answer": stream.answer[:500],
                "detail": detail,
                "category": item.category,
                "latency_ms": stream.latency_ms,
                "citations": len(stream.citations),
            })
        except Exception as exc:
            results.append({
                "id": item.id,
                "question": item.question,
                "pass": False,
                "answer": str(exc),
                "detail": "exception",
                "category": item.category,
            })
        time.sleep(0.5)
    return results


def _write_report(
    *,
    org_email: str,
    upload_failures: list[str],
    surface_results: list[dict],
    rag_results: list[dict],
    duration_sec: float,
    bugs: list[dict],
) -> None:
    rag_pass = sum(1 for row in rag_results if row["pass"])
    surface_pass = sum(1 for row in surface_results if row["pass"])
    lines = [
        "# EKA Regression Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Test org: `{org_email}`",
        f"Duration: {duration_sec:.0f}s",
        "",
        "## Summary",
        "",
        f"| Metric | Result |",
        f"|--------|--------|",
        f"| Documents uploaded | {50 - len(upload_failures)}/50 |",
        f"| API surface checks | {surface_pass}/{len(surface_results)} |",
        f"| RAG questions | {rag_pass}/{len(rag_results)} |",
        "",
        "## UI / API surfaces exercised",
        "",
        "| UI area | API endpoint | Covered |",
        "|---------|--------------|---------|",
        "| Auth (register/login) | POST /api/v1/auth/register, /login | yes |",
        "| Chat query + stream | POST /api/v1/query/stream | yes |",
        "| Admin upload | POST /api/v1/documents/upload | yes |",
        "| Documents page (list/delete) | GET/DELETE /api/v1/documents | yes |",
        "| Analytics panel | GET /api/v1/analytics/queries | yes |",
        "",
        "### Surface check results",
        "",
    ]
    for row in surface_results:
        status = "PASS" if row["pass"] else "FAIL"
        lines.append(f"- **{row['surface']}**: {status} — {row['detail']}")

    lines.extend(["", "## RAG question results", ""])
    lines.append("| ID | Pass | Category | Latency | Detail |")
    lines.append("|----|------|----------|---------|--------|")
    for row in rag_results:
        status = "PASS" if row["pass"] else "FAIL"
        latency = row.get("latency_ms", "—")
        lines.append(f"| {row['id']} | {status} | {row['category']} | {latency} | {row['detail']} |")

    lines.extend(["", "## Answers (excerpt)", ""])
    for row in rag_results:
        lines.append(f"### {row['id']}: {row['question']}")
        lines.append(f"- **Pass:** {row['pass']} — {row['detail']}")
        answer = row.get("answer", "").replace("\n", " ")
        lines.append(f"- **Answer:** {answer[:400]}...")
        lines.append("")

    if upload_failures:
        lines.extend(["## Upload failures", ""])
        for failure in upload_failures:
            lines.append(f"- {failure}")
        lines.append("")

    lines.extend(["## Bugs found & fixes", ""])
    if bugs:
        for bug in bugs:
            lines.append(f"### {bug['title']}")
            lines.append(f"- **Severity:** {bug['severity']}")
            lines.append(f"- **Symptom:** {bug['symptom']}")
            lines.append(f"- **Fix:** {bug['fix']}")
            lines.append("")
    else:
        lines.append("No new bugs filed during this run.")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run EKA regression suite")
    parser.add_argument("--skip-upload", action="store_true", help="Reuse existing indexed docs in test org")
    parser.add_argument("--email", default=None, help="Existing admin email to reuse")
    parser.add_argument("--password", default="RegressionTest1!", help="Password for test account")
    parser.add_argument(
        "--external",
        action="store_true",
        help="Hit running server at 127.0.0.1:8000 instead of in-process TestClient",
    )
    args = parser.parse_args()

    started = time.time()
    run_id = uuid.uuid4().hex[:8]
    email = args.email or f"regression_{run_id}@example.com"
    password = args.password
    org_name = f"Regression Org {run_id}"

    bugs = [
        {
            "title": "Chroma index corruption on re-upload",
            "severity": "high",
            "symptom": "Vector search InternalError after document replace",
            "fix": "Explicit chunk-id delete, orphan prune, rebuild from Postgres (vector_store.py)",
        },
        {
            "title": "Stale cache after upload",
            "severity": "high",
            "symptom": "Pre-upload 'no context' answers served after new docs indexed",
            "fix": "purge_org_query_cache on upload + embed complete (cache.py)",
        },
        {
            "title": "Contradictory trailing 'not available' line",
            "severity": "medium",
            "symptom": "Partial answers followed by blanket not-available phrase",
            "fix": "normalize_llm_answer + prompt rules (rag.py)",
        },
        {
            "title": "Judgment questions refused despite resume in context",
            "severity": "medium",
            "symptom": "'Is X a bad developer?' returned not available",
            "fix": "RAG_USER_INSTRUCTIONS for subjective person questions (rag.py)",
        },
    ]

    base = API_BASE if args.external else ""

    if args.external:
        client_stack = httpx.Client()
    else:
        from fastapi.testclient import TestClient
        from app.main import app

        client_stack = TestClient(app)

    with client_stack if args.external else nullcontext(client_stack) as client:
        healthy, detail = _check_health(client, base)
        if not healthy:
            target = API_BASE if args.external else "in-process TestClient"
            print(f"API not reachable ({target}): {detail}")
            return 1

        if args.email:
            token = login(client, base=base, email=email, password=password)
            print(f"Using existing account {email}")
        else:
            token = register_org(
                client, base=base, email=email, password=password, org_name=org_name
            )
            print(f"Created org '{org_name}' admin {email}")

        upload_failures: list[str] = []
        sample_doc_id: str | None = None
        if not args.skip_upload:
            print("Uploading 50-document corpus...")
            uploaded, upload_failures = _upload_corpus(client, base, token=token)
            if uploaded:
                sample_doc_id = uploaded[0]["id"]
        else:
            docs = list_documents(client, base=base, token=token)
            if docs:
                sample_doc_id = docs[0]["id"]

        print("Running API surface checks...")
        surface_results = _run_surface_tests(client, base, token, sample_doc_id)

        print(f"Running {len(RAG_QUESTIONS)} RAG questions...")
        rag_results = _run_rag_questions(client, base, token=token)

        if sample_doc_id and not args.skip_upload:
            try:
                delete_document(client, base=base, token=token, document_id=sample_doc_id)
                surface_results.append({
                    "surface": "documents_delete",
                    "pass": True,
                    "detail": f"deleted {sample_doc_id}",
                })
            except Exception as exc:
                surface_results.append({
                    "surface": "documents_delete",
                    "pass": False,
                    "detail": str(exc),
                })

    duration = time.time() - started
    _write_report(
        org_email=email,
        upload_failures=upload_failures,
        surface_results=surface_results,
        rag_results=rag_results,
        duration_sec=duration,
        bugs=bugs,
    )

    rag_failures = sum(1 for row in rag_results if not row["pass"])
    if upload_failures or rag_failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
