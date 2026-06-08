#!/usr/bin/env python3
"""Large-scale regression: 10 big PDFs (200-300 pages) + 100 grounded Q&A validations."""

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
from tests.regression.corpus_large import LARGE_DOCUMENTS, LargeDocument, write_large_corpus
from tests.regression.question_bank_large import LargeRegressionQuestion, build_large_question_bank
from tests.regression.validation import validate_answer_against_fact

REPORT_PATH = Path(__file__).parent / "LARGE_REGRESSION_REPORT.md"
CORPUS_DIR = Path(__file__).parent / "_corpus_large_pdfs"


def _documents_for_run(page_count: int) -> tuple[LargeDocument, ...]:
    return tuple(
        LargeDocument(doc.slug, doc.filename, doc.domain, page_count)
        for doc in LARGE_DOCUMENTS
    )


def _write_report(
    *,
    org_email: str,
    page_count: int,
    upload_results: list[dict],
    rag_results: list[dict],
    duration_sec: float,
) -> None:
    passed = sum(1 for row in rag_results if row["pass"])
    pdf_verified = sum(1 for row in rag_results if row.get("pdf_verified"))
    upload_ok = sum(1 for row in upload_results if row.get("status") == "ready")

    lines = [
        "# Large PDF Regression Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Test org: `{org_email}`",
        f"Pages per document: {page_count}",
        f"Documents: {len(upload_results)}",
        f"Questions: {len(rag_results)}",
        f"Duration: {duration_sec / 60:.1f} minutes",
        "",
        "## Summary",
        "",
        "| Metric | Result |",
        "|--------|--------|",
        f"| PDFs indexed (ready) | {upload_ok}/{len(upload_results)} |",
        f"| Questions passed (answer vs ground truth) | **{passed}/{len(rag_results)}** |",
        f"| Ground-truth facts verified in source PDF page | {pdf_verified}/{len(rag_results)} |",
        f"| Pass rate | {100 * passed / max(len(rag_results), 1):.1f}% |",
        "",
        "## Method",
        "",
        "- 10 synthetic handbooks, ~200–300 pages each, one KEY_FACT per page.",
        "- 100 questions (10 per document) ask for certification scores recorded on specific pages.",
        "- **Pass**: assistant answer contains ground-truth `cert_id` and `score` from the original PDF.",
        "- **PDF verified**: fact text found on the cited page when re-reading the generated PDF from disk.",
        "",
        "## Upload results",
        "",
        "| File | Pages | Status | Chunks | Seconds |",
        "|------|-------|--------|--------|---------|",
    ]
    for row in upload_results:
        lines.append(
            f"| {row['filename']} | {row.get('pages', '—')} | {row.get('status', '—')} | "
            f"{row.get('chunk_count', '—')} | {row.get('seconds', '—')} |"
        )

    lines.extend(["", "## Question results", ""])
    lines.append("| ID | Pass | PDF OK | Latency ms | Source | Detail |")
    lines.append("|----|------|--------|------------|--------|--------|")
    for row in rag_results:
        status = "PASS" if row["pass"] else "FAIL"
        pdf_ok = "yes" if row.get("pdf_verified") else "no"
        lines.append(
            f"| {row['id']} | {status} | {pdf_ok} | {row.get('latency_ms', '—')} | "
            f"{row.get('source_file', '')} p{row.get('source_page', '')} | {row['detail'][:80]} |"
        )

    lines.extend(["", "## Ground truth vs answers", ""])
    for row in rag_results:
        lines.append(f"### {row['id']}")
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
                f"- **{row['id']}** ({row['source_file']} p{row['source_page']}): {row['detail']}"
            )
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH}")


def _upload_large_corpus(client: object, base: str, token: str, documents: tuple[LargeDocument, ...]) -> list[dict]:
    write_large_corpus(CORPUS_DIR, documents=documents)
    results: list[dict] = []
    for index, document in enumerate(documents, start=1):
        path = CORPUS_DIR / document.filename
        started = time.perf_counter()
        print(f"  [{index}/{len(documents)}] Uploading {document.filename} ({document.page_count} pages)...")
        try:
            meta = upload_pdf(
                client,
                base=base,
                token=token,
                pdf_path=path,
                timeout=3600.0,
            )
            if meta.get("status") == "processing":
                meta = wait_document_ready(
                    client,
                    base=base,
                    token=token,
                    document_id=meta["id"],
                    timeout_sec=3600.0,
                )
            elapsed = int(time.perf_counter() - started)
            results.append({
                "filename": document.filename,
                "pages": document.page_count,
                "status": meta.get("status"),
                "chunk_count": meta.get("chunk_count"),
                "seconds": elapsed,
            })
            print(
                f"       -> {meta.get('status')} ({meta.get('chunk_count')} chunks) in {elapsed}s"
            )
        except Exception as exc:
            results.append({
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
    token: str,
    questions: list[LargeRegressionQuestion],
) -> list[dict]:
    results: list[dict] = []
    for index, item in enumerate(questions, start=1):
        print(f"  [{index}/{len(questions)}] {item.id}")
        pdf_path = CORPUS_DIR / item.source_file
        try:
            stream = query_stream(client, base=base, token=token, question=item.question)
            if stream.error:
                results.append({
                    "id": item.id,
                    "question": item.question,
                    "pass": False,
                    "detail": stream.error,
                    "answer": stream.error,
                    "ground_truth": item.canonical_answer_hint,
                    "source_file": item.source_file,
                    "source_page": item.source_page,
                    "pdf_verified": False,
                    "latency_ms": stream.latency_ms,
                })
                continue

            passed, detail, pdf_ok = validate_answer_against_fact(
                stream.answer,
                fact=item.ground_truth,
                expect_any=item.expect_any,
                pdf_path=pdf_path,
            )
            results.append({
                "id": item.id,
                "question": item.question,
                "pass": passed,
                "detail": detail,
                "answer": stream.answer,
                "ground_truth": item.canonical_answer_hint,
                "source_file": item.source_file,
                "source_page": item.source_page,
                "pdf_verified": pdf_ok,
                "latency_ms": stream.latency_ms,
            })
        except Exception as exc:
            results.append({
                "id": item.id,
                "question": item.question,
                "pass": False,
                "detail": str(exc),
                "answer": str(exc),
                "ground_truth": item.canonical_answer_hint,
                "source_file": item.source_file,
                "source_page": item.source_page,
                "pdf_verified": False,
            })
        time.sleep(0.3)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Large PDF regression (10 docs, 100 questions)")
    parser.add_argument("--pages", type=int, default=250, help="Pages per PDF (200-300)")
    parser.add_argument("--questions-per-doc", type=int, default=10, help="Questions per document")
    parser.add_argument("--external", action="store_true", help="Use running server on :8000")
    parser.add_argument("--skip-upload", action="store_true")
    parser.add_argument("--email", default=None)
    parser.add_argument("--password", default="RegressionTest1!")
    args = parser.parse_args()

    if not 200 <= args.pages <= 300:
        print("Warning: pages should be between 200 and 300 for this benchmark.")

    started = time.time()
    run_id = uuid.uuid4().hex[:8]
    email = args.email or f"large_regression_{run_id}@example.com"
    password = args.password
    org_name = f"Large Regression {run_id}"

    documents = _documents_for_run(args.pages)
    questions = build_large_question_bank(questions_per_doc=args.questions_per_doc)
    print(f"Benchmark: {len(documents)} PDFs × {args.pages} pages, {len(questions)} questions")

    base = API_BASE if args.external else ""

    if args.external:
        client_stack = httpx.Client(timeout=3600.0)
    else:
        from fastapi.testclient import TestClient
        from app.main import app

        client_stack = TestClient(app)

    with client_stack if args.external else nullcontext(client_stack) as client:
        if args.email:
            token = login(client, base=base, email=email, password=password)
        else:
            token = register_org(
                client, base=base, email=email, password=password, org_name=org_name
            )
            print(f"Created org admin {email}")
        clear_rate_limit_for_token(token)

        upload_results: list[dict] = []
        if not args.skip_upload:
            print("Generating and uploading large PDFs (this may take a long time)...")
            upload_results = _upload_large_corpus(client, base, token, documents)
        else:
            write_large_corpus(CORPUS_DIR, documents=documents)
            upload_results = [
                {"filename": doc.filename, "pages": doc.page_count, "status": "skipped"}
                for doc in documents
            ]

        ready_count = sum(1 for row in upload_results if row.get("status") == "ready")
        if ready_count == 0 and not args.skip_upload:
            print("No documents reached ready status; aborting questions.")
            _write_report(
                org_email=email,
                page_count=args.pages,
                upload_results=upload_results,
                rag_results=[],
                duration_sec=time.time() - started,
            )
            return 1

        print(f"Running {len(questions)} questions...")
        rag_results = _run_questions(client, base, token, questions)

    duration = time.time() - started
    _write_report(
        org_email=email,
        page_count=args.pages,
        upload_results=upload_results,
        rag_results=rag_results,
        duration_sec=duration,
    )

    passed = sum(1 for row in rag_results if row["pass"])
    print(f"Passed {passed}/{len(rag_results)} questions")
    if passed < len(rag_results) or ready_count < len(documents):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
