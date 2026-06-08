import uuid

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.redis_client import is_redis_available
from app.core.storage import save_pdf
from app.models.document import Document, DocumentAccessLevel, DocumentStatus
from app.repositories.chunk import bulk_create_chunks
from app.repositories.document import (
    create_document,
    get_document_by_filename,
    list_documents_by_filename,
    update_document_status,
)
from app.services.chunking import chunk_pages
from app.services.document_embed import run_document_embedding
from app.services.cache import invalidate_org_answer_cache
from app.services.document_lifecycle import (
    prepare_document_for_reingest,
    remove_document,
)
from app.services.pdf_extract import extract_text_from_pdf


def should_embed_async() -> bool:
    settings = get_settings()
    return settings.embed_async and is_redis_available()


def ingest_document(
    db: Session,
    *,
    organization_id: uuid.UUID,
    uploaded_by: uuid.UUID,
    filename: str,
    pdf_data: bytes,
    access_level: DocumentAccessLevel = DocumentAccessLevel.PUBLIC,
) -> Document:
    existing = get_document_by_filename(
        db,
        organization_id=organization_id,
        filename=filename,
    )
    if existing is not None:
        return _replace_document(
            db,
            document=existing,
            organization_id=organization_id,
            uploaded_by=uploaded_by,
            filename=filename,
            pdf_data=pdf_data,
            access_level=access_level,
        )

    document = create_document(
        db,
        organization_id=organization_id,
        filename=filename,
        uploaded_by=uploaded_by,
        status=DocumentStatus.PENDING,
        access_level=access_level,
    )
    db.flush()
    return _process_document_content(
        db,
        document=document,
        organization_id=organization_id,
        pdf_data=pdf_data,
    )


def _replace_document(
    db: Session,
    *,
    document: Document,
    organization_id: uuid.UUID,
    uploaded_by: uuid.UUID,
    filename: str,
    pdf_data: bytes,
    access_level: DocumentAccessLevel,
) -> Document:
    for stale in list_documents_by_filename(
        db,
        organization_id=organization_id,
        filename=filename,
        exclude_document_id=document.id,
    ):
        remove_document(
            db,
            organization_id=organization_id,
            document_id=stale.id,
        )

    prepare_document_for_reingest(
        db,
        organization_id=organization_id,
        document=document,
        access_level=access_level,
        uploaded_by=uploaded_by,
    )
    return _process_document_content(
        db,
        document=document,
        organization_id=organization_id,
        pdf_data=pdf_data,
    )


def _process_document_content(
    db: Session,
    *,
    document: Document,
    organization_id: uuid.UUID,
    pdf_data: bytes,
) -> Document:
    embed_async = should_embed_async()
    invalidate_org_answer_cache(organization_id=organization_id)

    try:
        save_pdf(
            organization_id=organization_id,
            document_id=document.id,
            data=pdf_data,
        )
        update_document_status(db, document=document, status=DocumentStatus.PROCESSING)

        pages = extract_text_from_pdf(pdf_data)
        text_chunks = chunk_pages(pages)
        bulk_create_chunks(db, document_id=document.id, chunks=text_chunks)

        if embed_async:
            db.commit()
            db.refresh(document)
            return document

        run_document_embedding(
            db,
            document_id=document.id,
            organization_id=organization_id,
        )
    except Exception:
        update_document_status(db, document=document, status=DocumentStatus.FAILED)
        db.commit()
        db.refresh(document)
        raise

    db.commit()
    db.refresh(document)
    return document
