"""HTTP helpers for regression tests against the running API."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import httpx

API_BASE = "http://127.0.0.1:8000"
Client = httpx.Client | object  # httpx.Client or FastAPI TestClient


@dataclass
class StreamResult:
    answer: str
    citations: list[dict]
    error: str | None = None
    latency_ms: int | None = None


def _url(base: str, path: str) -> str:
    return f"{base}{path}" if base else path


def register_org(client: Client, *, base: str, email: str, password: str, org_name: str) -> str:
    response = client.post(
        _url(base, "/api/v1/auth/register"),
        json={
            "email": email,
            "password": password,
            "organization_name": org_name,
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]


def login(client: Client, *, base: str, email: str, password: str) -> str:
    response = client.post(
        _url(base, "/api/v1/auth/login"),
        json={"email": email, "password": password},
    )
    response.raise_for_status()
    return response.json()["access_token"]


def clear_rate_limit_for_token(token: str) -> None:
    """Reset Redis query rate-limit counter so regression suites can exceed 100/hour."""
    from app.core.security import decode_access_token
    from app.core.redis_client import redis_or_none

    payload = decode_access_token(token)
    org_id = payload.get("organization_id")
    user_id = payload.get("sub")
    if not org_id or not user_id:
        return

    client = redis_or_none()
    if client is None:
        return

    key = f"rl:{org_id}:{user_id}"
    try:
        client.delete(key)
    except Exception:
        pass


def upload_pdf(
    client: Client,
    *,
    base: str,
    token: str,
    pdf_path: Path,
    access_level: str = "public",
    timeout: float = 120.0,
) -> dict:
    with pdf_path.open("rb") as handle:
        response = client.post(
            _url(base, "/api/v1/documents/upload"),
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (pdf_path.name, handle, "application/pdf")},
            data={"access_level": access_level},
            timeout=timeout,
        )
    response.raise_for_status()
    return response.json()


def wait_document_ready(
    client: Client,
    *,
    base: str,
    token: str,
    document_id: str,
    timeout_sec: float = 120.0,
) -> dict:
    import time

    deadline = time.time() + timeout_sec
    last: dict = {}
    while time.time() < deadline:
        response = client.get(
            _url(base, f"/api/v1/documents/{document_id}"),
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        last = response.json()
        if last.get("status") in {"ready", "failed"}:
            return last
        time.sleep(2.0)
    return last


def list_documents(client: Client, *, base: str, token: str) -> list[dict]:
    response = client.get(
        _url(base, "/api/v1/documents"),
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json().get("items", [])


def delete_document(client: Client, *, base: str, token: str, document_id: str) -> None:
    response = client.delete(
        _url(base, f"/api/v1/documents/{document_id}"),
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()


def query_stream(client: Client, *, base: str, token: str, question: str) -> StreamResult:
    response = client.post(
        _url(base, "/api/v1/query/stream"),
        headers={"Authorization": f"Bearer {token}"},
        json={"question": question},
        timeout=180.0,
    )
    response.raise_for_status()

    answer_parts: list[str] = []
    citations: list[dict] = []
    error: str | None = None
    latency_ms: int | None = None

    for part in response.text.split("\n\n"):
        if not part.strip():
            continue
        event = "message"
        data_line = ""
        for line in part.split("\n"):
            if line.startswith("event: "):
                event = line[7:].strip()
            if line.startswith("data: "):
                data_line = line[6:]
        if not data_line:
            continue
        payload = json.loads(data_line)
        if event == "token":
            answer_parts.append(payload.get("text", ""))
        elif event == "citations":
            citations = payload.get("citations", [])
        elif event == "done":
            answer_parts = [payload.get("answer", "".join(answer_parts))]
            citations = payload.get("citations", citations)
            latency_ms = payload.get("latency_ms")
        elif event == "error":
            error = payload.get("detail", "Stream error")

    return StreamResult(
        answer="".join(answer_parts).strip(),
        citations=citations,
        error=error,
        latency_ms=latency_ms,
    )


def score_answer(
    answer: str,
    expect_any: tuple[str, ...],
    expect_none: tuple[str, ...],
    *,
    expect_refusal: bool = False,
) -> tuple[bool, str]:
    if not answer:
        return False, "empty answer"
    lower = answer.lower()
    if expect_refusal:
        if "not available" in lower:
            return True, "correct refusal"
        return False, "expected refusal but got content"
    if expect_none and any(term.lower() in lower for term in expect_none):
        return False, f"forbidden phrase present: {expect_none}"
    if not expect_any:
        return False, "no expectations configured"
    matched = [term for term in expect_any if term.lower() in lower]
    if matched:
        return True, f"matched: {matched}"
    return False, f"missing any of {expect_any}"
