import uuid
from pathlib import Path

from app.core.config import get_settings


def get_document_path(
    *,
    organization_id: uuid.UUID,
    document_id: uuid.UUID,
    extension: str = ".pdf",
) -> Path:
    settings = get_settings()
    org_dir = Path(settings.upload_dir) / str(organization_id)
    org_dir.mkdir(parents=True, exist_ok=True)
    return org_dir / f"{document_id}{extension}"


def save_pdf(
    *,
    organization_id: uuid.UUID,
    document_id: uuid.UUID,
    data: bytes,
) -> Path:
    path = get_document_path(
        organization_id=organization_id,
        document_id=document_id,
    )
    path.write_bytes(data)
    return path


def read_pdf(
    *,
    organization_id: uuid.UUID,
    document_id: uuid.UUID,
) -> bytes:
    path = get_document_path(
        organization_id=organization_id,
        document_id=document_id,
    )
    return path.read_bytes()
