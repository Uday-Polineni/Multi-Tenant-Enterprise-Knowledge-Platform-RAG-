#!/usr/bin/env python3
"""Multi-org regression: 3 orgs × 15 topics (10–15 pages) + 100 grounded Q&A."""

from __future__ import annotations

import argparse
import os
import sys
import time
import uuid
from contextlib import nullcontext
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import httpx

os.environ.setdefault("EMBED_ASYNC", "false")
os.environ.setdefault("RATE_LIMIT_PER_HOUR", "10000")
os.environ.setdefault("PROTOTYPE_MAX_PDF_PAGES", "0")
os.environ.setdefault("PROTOTYPE_MAX_DOCUMENTS_PER_ORG", "0")

from tests.regression.api_helpers import (
    API_BASE,
    clear_rate_limit_for_token,
    login,
    query_stream,
    register_org,
    upload_pdf,
    wait_document_ready,
)
from tests.regression.corpus_multi_org import ORGANIZATIONS, all_documents, write_org_corpus
from tests.regression.question_bank_multi_org import MultiOrgQuestion, build_multi_org_question_bank
from tests.regression.validation_multi_org import validate_multi_org_answer

REPORT_PATH = Path(__file__).parent / "MULTI_ORG_REGRESSION_REPORT.md"
CORPUS_DIR = Path(__file__).parent / "_corpus_multi_org"
PASSWORD = "RegressionTest1!"


def _write_report(
    *,
    org_accounts: dict[str, str],
    upload_results: list[dict],
    rag_results: list[dict],
    duration_sec: float,
) -> None:
    passed = sum(1 for row in rag_results if row["pass"])
    pdf_verified = sum(1 for row in rag_results if row.get("pdf_verified"))
    upload_ok = sum(1 for row in upload_results if row.get("status") == "ready")

    by_org: dict[str, list[dict]] = defaultdict(list)
    for row in rag_results:
        by_org[row["org_code"]].append(row)

    lines = [
        "# Multi-Organization Regression Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Organizations: {len(ORGANIZATIONS)}",
        f"Topics per org: 15",
        f"Pages per document: 10–15",
        f"Total documents: {len(all_documents())}",
        f"Questions: {len(rag_results)}",
        f"Duration: {duration_sec / 60:.1f} minutes",
        "",
        "## Summary",
        "",
        "| Metric | Result |",
        "|--------|--------|",
        f"| PDFs indexed (ready) | {upload_ok}/{len(upload_results)} |",
        f"| Questions passed (answer vs ground truth) | **{passed}/{len(rag_results)}** |",
        f"| Ground-truth facts verified in source PDF | {pdf_verified}/{len(rag_results)} |",
        f"| Pass rate | {100 * passed / max(len(rag_results), 1):.1f}% |",
        "",
        "## Organizations",
        "",
        "| Org | Admin email | Docs uploaded | Questions | Passed |",
        "|-----|-------------|---------------|-----------|--------|",
    ]
    for org in ORGANIZATIONS:
        org_uploads = [r for r in upload_results if r.get("org_code") == org.code]
        org_ready = sum(1 for r in org_uploads if r.get("status") == "ready")
        org_questions = by_org[org.code]
        org_passed = sum(1 for r in org_questions if r["pass"])
        lines.append(
            f"| {org.name} | `{org_accounts[org.code]}` | {org_ready}/15 | "
            f"{len(org_questions)} | {org_passed}/{len(org_questions)} |"
        )

    lines.extend([
        "",
        "## Method",
        "",
        "- 3 organizations, each with 15 topic PDFs (10–15 pages).",
        "- Org-specific KEY_FACT on page 1; per-page AUDIT tokens on inner/last pages.",
        "- 100 questions: 45 primary, 45 page-fact, 10 late-page (Acme).",
        "- **Pass**: answer contains expected ground-truth terms from the source PDF.",
        "- Each question runs against its organization's indexed documents only.",
        "",
        "## Upload results",
        "",
        "| Org | File | Pages | Status | Chunks | Seconds |",
        "|-----|------|-------|--------|--------|---------|",
    ])
    for row in upload_results:
        lines.append(
            f"| {row.get('org_code', '—')} | {row['filename']} | {row.get('pages', '—')} | "
            f"{row.get('status', '—')} | {row.get('chunk_count', '—')} | {row.get('seconds', '—')} |"
        )

    lines.extend(["", "## Question results", ""])
    lines.append("| ID | Org | Pass | PDF OK | Latency ms | Source | Detail |")
    lines.append("|----|-----|------|--------|------------|--------|--------|")
    for row in rag_results:
        status = "PASS" if row["pass"] else "FAIL"
        pdf_ok = "yes" if row.get("pdf_verified") else "no"
        lines.append(
            f"| {row['id']} | {row['org_code']} | {status} | {pdf_ok} | "
            f"{row.get('latency_ms', '—')} | {row.get('source_file', '')} p{row.get('source_page', '')} | "
            f"{row['detail'][:70]} |"
        )

    lines.extend(["", "## Ground truth vs answers", ""])
    for row in rag_results:
        lines.append(f"### {row['id']}")
        lines.append(f"- **Org:** {row['org_name']}")
        lines.append(f"- **Question:** {row['question']}")
        lines.append(f"- **Ground truth:** {row.get('ground_truth', '')}")
        lines.append(f"- **Pass:** {row['pass']} — {row['detail']}")
        answer = row.get("answer", "").replace("\n", " ")
        lines.append(f"- **Assistant answer:** {answer[:500]}")
        lines.append("")

    failures = [row for row in rag_results if not row["pass"]]
    if failures:
        lines.extend(["## Failures", ""])
        for row in failures:
            lines.append(
                f"- **{row['id']}** ({row['org_name']}, {row['source_file']} p{row['source_page']}): "
                f"{row['detail']}"
            )
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH}")


def _register_orgs(
    client: object,
    base: str,
    *,
    run_id: str,
    emails: dict[str, str] | None,
) -> tuple[dict[str, str], dict[str, str]]:
    tokens: dict[str, str] = {}
    accounts: dict[str, str] = {}
    for org in ORGANIZATIONS:
        email = (emails or {}).get(org.code) or f"multi_org_{org.code}_{run_id}@example.com"
        accounts[org.code] = email
        token = register_org(
            client,
            base=base,
            email=email,
            password=PASSWORD,
            org_name=f"{org.name} Regression {run_id}",
        )
        tokens[org.code] = token
        clear_rate_limit_for_token(token)
        print(f"  Registered {org.name} -> {email}")
    return tokens, accounts


def _upload_org_corpus(
    client: object,
    base: str,
    tokens: dict[str, str],
    paths_by_org: dict[str, list[Path]],
) -> list[dict]:
    results: list[dict] = []
    documents = all_documents()
    total = len(documents)
    for index, document in enumerate(documents, start=1):
        path = CORPUS_DIR / document.org.code / document.filename
        token = tokens[document.org.code]
        started = time.perf_counter()
        print(
            f"  [{index}/{total}] {document.org.code}: {document.filename} "
            f"({document.page_count} pages)"
        )
        try:
            meta = upload_pdf(client, base=base, token=token, pdf_path=path, timeout=600.0)
            if meta.get("status") == "processing":
                meta = wait_document_ready(
                    client,
                    base=base,
                    token=token,
                    document_id=meta["id"],
                    timeout_sec=600.0,
                )
            elapsed = int(time.perf_counter() - started)
            results.append({
                "org_code": document.org.code,
                "filename": document.filename,
                "pages": document.page_count,
                "status": meta.get("status"),
                "chunk_count": meta.get("chunk_count"),
                "seconds": elapsed,
            })
            print(f"       -> {meta.get('status')} ({meta.get('chunk_count')} chunks) in {elapsed}s")
        except Exception as exc:
            results.append({
                "org_code": document.org.code,
                "filename": document.filename,
                "pages": document.page_count,
                "status": "error",
                "error": str(exc),
                "seconds": int(time.perf_counter() - started),
            })
            print(f"       -> FAILED: {exc}")
    return results


def _run_questions(
    client: object,
    base: str,
    tokens: dict[str, str],
    questions: list[MultiOrgQuestion],
) -> list[dict]:
    results: list[dict] = []
    for index, item in enumerate(questions, start=1):
        print(f"  [{index}/{len(questions)}] {item.id}")
        token = tokens[item.org_code]
        pdf_path = CORPUS_DIR / item.org_code / item.source_file
        try:
            stream = query_stream(client, base=base, token=token, question=item.question)
            if stream.error:
                results.append(_result_row(item, passed=False, detail=stream.error, answer=stream.error))
                continue

            passed, detail, pdf_ok = validate_multi_org_answer(
                stream.answer,
                item=item,
                pdf_path=pdf_path,
            )
            results.append(
                _result_row(
                    item,
                    passed=passed,
                    detail=detail,
                    answer=stream.answer,
                    pdf_verified=pdf_ok,
                    latency_ms=stream.latency_ms,
                )
            )
        except Exception as exc:
            results.append(_result_row(item, passed=False, detail=str(exc), answer=str(exc)))
        time.sleep(0.2)
    return results


def _result_row(
    item: MultiOrgQuestion,
    *,
    passed: bool,
    detail: str,
    answer: str,
    pdf_verified: bool = False,
    latency_ms: int | None = None,
) -> dict:
    return {
        "id": item.id,
        "org_code": item.org_code,
        "org_name": item.org_name,
        "question": item.question,
        "pass": passed,
        "detail": detail,
        "answer": answer,
        "ground_truth": item.ground_truth,
        "source_file": item.source_file,
        "source_page": item.source_page,
        "pdf_verified": pdf_verified,
        "latency_ms": latency_ms,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-org regression (3 orgs, 100 questions)")
    parser.add_argument("--external", action="store_true", help="Use running server on :8000")
    parser.add_argument("--skip-upload", action="store_true")
    parser.add_argument("--run-id", default=None, help="Reuse org emails multi_org_{code}_{run_id}@example.com")
    args = parser.parse_args()

    started = time.time()
    run_id = args.run_id or uuid.uuid4().hex[:8]
    questions = build_multi_org_question_bank()
    print(
        f"Benchmark: {len(ORGANIZATIONS)} orgs × 15 topics, "
        f"{len(all_documents())} PDFs, {len(questions)} questions"
    )

    base = API_BASE if args.external else ""
    if args.external:
        client_stack = httpx.Client(timeout=600.0)
    else:
        from fastapi.testclient import TestClient
        from app.main import app

        client_stack = TestClient(app)

    emails = {org.code: f"multi_org_{org.code}_{run_id}@example.com" for org in ORGANIZATIONS}

    with client_stack if args.external else nullcontext(client_stack) as client:
        if args.skip_upload:
            tokens = {
                org.code: login(client, base=base, email=emails[org.code], password=PASSWORD)
                for org in ORGANIZATIONS
            }
            for token in tokens.values():
                clear_rate_limit_for_token(token)
            accounts = emails
            print("Skipped upload — using existing orgs")
        else:
            print("Generating PDFs and registering organizations...")
            write_org_corpus(CORPUS_DIR)
            tokens, accounts = _register_orgs(client, base, run_id=run_id, emails=None)

        upload_results: list[dict] = []
        if not args.skip_upload:
            print("Uploading documents...")
            paths_by_org = write_org_corpus(CORPUS_DIR)
            upload_results = _upload_org_corpus(client, base, tokens, paths_by_org)
        else:
            for document in all_documents():
                upload_results.append({
                    "org_code": document.org.code,
                    "filename": document.filename,
                    "pages": document.page_count,
                    "status": "skipped",
                })

        ready_count = sum(1 for row in upload_results if row.get("status") == "ready")
        if ready_count == 0 and not args.skip_upload:
            _write_report(
                org_accounts=accounts,
                upload_results=upload_results,
                rag_results=[],
                duration_sec=time.time() - started,
            )
            return 1

        for token in tokens.values():
            clear_rate_limit_for_token(token)

        print(f"Running {len(questions)} questions...")
        rag_results = _run_questions(client, base, tokens, questions)

    duration = time.time() - started
    _write_report(
        org_accounts=accounts,
        upload_results=upload_results,
        rag_results=rag_results,
        duration_sec=duration,
    )

    passed = sum(1 for row in rag_results if row["pass"])
    print(f"Passed {passed}/{len(rag_results)} questions")
    print(f"Run ID: {run_id}")
    return 0 if passed == len(rag_results) and ready_count >= len(all_documents()) else 1


if __name__ == "__main__":
    sys.exit(main())
