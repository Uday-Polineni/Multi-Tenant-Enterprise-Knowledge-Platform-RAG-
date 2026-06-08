import hashlib
import re
import uuid


def normalize_question(question: str) -> str:
    text = question.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def question_hash(question: str) -> str:
    normalized = normalize_question(question)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def org_cache_version_key(organization_id: uuid.UUID) -> str:
    return f"cache:org_version:{organization_id}"


def answer_cache_key(
    *,
    organization_id: uuid.UUID,
    role: str,
    question: str,
    cache_version: int,
) -> str:
    digest = question_hash(question)
    return f"cache:answer:{organization_id}:{role}:v{cache_version}:{digest}"


def semantic_cache_index_key(
    *,
    organization_id: uuid.UUID,
    role: str,
    cache_version: int,
) -> str:
    return f"cache:semantic:{organization_id}:{role}:v{cache_version}:index"


def embedding_cache_key(question: str) -> str:
    digest = question_hash(question)
    return f"cache:embed:{digest}"
