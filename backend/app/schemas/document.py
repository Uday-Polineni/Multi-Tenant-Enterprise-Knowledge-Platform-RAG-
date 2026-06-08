import uuid
from datetime import datetime

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    id: uuid.UUID
    filename: str
    status: str
    access_level: str
    organization_id: uuid.UUID
    chunk_count: int
    created_at: datetime


class DocumentSummary(BaseModel):
    id: uuid.UUID
    filename: str
    status: str
    access_level: str
    created_at: datetime

    model_config = {"from_attributes": True}
