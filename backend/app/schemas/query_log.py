import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class QueryLogSummary(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    question: str
    answer: str
    latency_ms: int
    token_usage: dict | None
    retrieved_chunk_ids: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class QueryLogListResponse(BaseModel):
    items: list[QueryLogSummary]
    limit: int
    offset: int
