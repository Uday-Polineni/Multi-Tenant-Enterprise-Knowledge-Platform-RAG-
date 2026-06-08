import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.storage import delete_pdf
from app.models.chunk import Chunk
from app.models.document import Document, DocumentAccessLevel, DocumentStatus
from app.repositories.chunk import delete_chunks_for_document as delete_pg_chunks
from app.repositories.document import get_document_by_id
from app.services.cache import invalidate_org_answer_cache
from app.services.vector_store import delete_chunks_for_document as delete_chroma_chunks


class DocumentNotFoundError(Exception):
    pass


def remove_document(
    db: Session,
    *,
    organization_id: uuid.UUID,
    document_id: uuid.UUID,
) -> None:
    document = get_document_by_id(
        db,
        document_id=document_id,
        organization_id=organization_id,
    )
    if document is None:
        raise DocumentNotFoundError(f"Document {document_id} not found")

    chunk_ids = list(
        db.scalars(select(Chunk.id).where(Chunk.document_id == document_id)).all()
    )
    delete_chroma_chunks(
        organization_id=organization_id,
        document_id=document_id,
        chunk_ids=chunk_ids,
    )
    delete_pdf(organization_id=organization_id, document_id=document_id)
    db.delete(document)
    db.flush()
    invalidate_org_answer_cache(organization_id=organization_id)


def clear_document_index(
    db: Session,
    *,
    organization_id: uuid.UUID,
    document: Document,
) -> None:
    chunk_ids = list(
        db.scalars(select(Chunk.id).where(Chunk.document_id == document.id)).all()
    )
    delete_chroma_chunks(
        organization_id=organization_id,
        document_id=document.id,
        chunk_ids=chunk_ids,
    )
    delete_pg_chunks(db, document_id=document.id)
    invalidate_org_answer_cache(organization_id=organization_id)


def prepare_document_for_reingest(
    db: Session,
    *,
    organization_id: uuid.UUID,
    document: Document,
    access_level: DocumentAccessLevel,
    uploaded_by: uuid.UUID,
) -> Document:
    clear_document_index(db, organization_id=organization_id, document=document)
    document.access_level = access_level
    document.uploaded_by = uploaded_by
    document.status = DocumentStatus.PROCESSING
    db.flush()
    return document
