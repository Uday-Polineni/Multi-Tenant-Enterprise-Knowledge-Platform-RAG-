import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.document import Document, DocumentAccessLevel, DocumentStatus


def create_document(
    db: Session,
    *,
    organization_id: uuid.UUID,
    filename: str,
    uploaded_by: uuid.UUID,
    status: DocumentStatus = DocumentStatus.PENDING,
    access_level: DocumentAccessLevel = DocumentAccessLevel.PUBLIC,
) -> Document:
    document = Document(
        organization_id=organization_id,
        filename=filename,
        uploaded_by=uploaded_by,
        status=status,
        access_level=access_level,
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


def get_document_by_filename(
    db: Session,
    *,
    organization_id: uuid.UUID,
    filename: str,
) -> Document | None:
    stmt = (
        select(Document)
        .where(
            Document.organization_id == organization_id,
            Document.filename == filename,
        )
        .order_by(Document.created_at.desc())
        .limit(1)
    )
    return db.scalars(stmt).first()


def count_documents_for_org(
    db: Session,
    *,
    organization_id: uuid.UUID,
) -> int:
    stmt = (
        select(func.count())
        .select_from(Document)
        .where(Document.organization_id == organization_id)
    )
    return db.scalar(stmt) or 0


def list_documents_for_org(
    db: Session,
    *,
    organization_id: uuid.UUID,
) -> list[Document]:
    stmt = (
        select(Document)
        .where(Document.organization_id == organization_id)
        .order_by(Document.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def list_queryable_documents_for_role(
    db: Session,
    *,
    organization_id: uuid.UUID,
    allowed_access_levels: list[str],
) -> list[Document]:
    """Ready documents the user can retrieve in RAG for their role."""
    if not allowed_access_levels:
        return []

    levels = [DocumentAccessLevel(level) for level in allowed_access_levels]
    stmt = (
        select(Document)
        .where(
            Document.organization_id == organization_id,
            Document.access_level.in_(levels),
            Document.status == DocumentStatus.READY,
        )
        .order_by(Document.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def list_documents_by_filename(
    db: Session,
    *,
    organization_id: uuid.UUID,
    filename: str,
    exclude_document_id: uuid.UUID | None = None,
) -> list[Document]:
    stmt = select(Document).where(
        Document.organization_id == organization_id,
        Document.filename == filename,
    )
    if exclude_document_id is not None:
        stmt = stmt.where(Document.id != exclude_document_id)
    return list(db.scalars(stmt).all())
