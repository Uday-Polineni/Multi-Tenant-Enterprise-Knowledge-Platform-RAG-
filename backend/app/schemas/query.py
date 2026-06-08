import uuid

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class Citation(BaseModel):
    document: str
    document_id: uuid.UUID
    page: int | None = None
    section: str | None = None
    chunk_id: uuid.UUID
    source_index: int | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
