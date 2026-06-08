import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.query_log import QueryLog


def create_query_log(
    db: Session,
    *,
    organization_id: uuid.UUID,
    user_id: uuid.UUID | None,
    question: str,
    answer: str,
    latency_ms: int,
    retrieved_chunk_ids: list[str],
    token_usage: dict | None = None,
) -> QueryLog:
    row = QueryLog(
        organization_id=organization_id,
        user_id=user_id,
        question=question,
        answer=answer,
        latency_ms=latency_ms,
        retrieved_chunk_ids=retrieved_chunk_ids,
        token_usage=token_usage,
    )
    db.add(row)
    db.flush()
    return row


def list_query_logs(
    db: Session,
    *,
    organization_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[QueryLog]:
    stmt = (
        select(QueryLog)
        .where(QueryLog.organization_id == organization_id)
        .order_by(QueryLog.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(stmt).all())
