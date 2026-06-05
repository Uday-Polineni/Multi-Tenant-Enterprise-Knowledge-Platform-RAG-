import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document, DocumentStatus


def create_document(
    db: Session,
    *,
    organization_id: uuid.UUID,
    filename: str,
    uploaded_by: uuid.UUID,
    status: DocumentStatus = DocumentStatus.PENDING,
) -> Document:
    document = Document(
        organization_id=organization_id,
        filename=filename,
        uploaded_by=uploaded_by,
        status=status,
    )
    db.add(document)
    db.flush()
    return document


def update_document_status(
    db: Session,
    *,
    document: Document,
    status: DocumentStatus,
) -> Document:
    document.status = status
    db.flush()
    return document


def get_document_by_id(
    db: Session,
    *,
    document_id: uuid.UUID,
    organization_id: uuid.UUID,
) -> Document | None:
    stmt = select(Document).where(
        Document.id == document_id,
        Document.organization_id == organization_id,
    )
    return db.scalars(stmt).first()
