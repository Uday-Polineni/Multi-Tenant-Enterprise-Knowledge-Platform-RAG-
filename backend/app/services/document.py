import uuid

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.storage import save_pdf
from app.models.chunk import Chunk
from app.models.document import Document, DocumentAccessLevel, DocumentStatus
from app.repositories.chunk import bulk_create_chunks
from app.repositories.document import (
    create_document,
    update_document_status,
)
from app.services.chunking import chunk_pages
from app.services.embedding import EmbeddingError, embed_document_chunks
from app.services.pdf_extract import extract_text_from_pdf


def ingest_document(
    db: Session,
    *,
    organization_id: uuid.UUID,
    uploaded_by: uuid.UUID,
    filename: str,
    pdf_data: bytes,
    access_level: DocumentAccessLevel = DocumentAccessLevel.PUBLIC,
) -> Document:
    document = create_document(
        db,
        organization_id=organization_id,
        filename=filename,
        uploaded_by=uploaded_by,
        status=DocumentStatus.PENDING,
        access_level=access_level,
    )
    db.flush()

    try:
        save_pdf(
            organization_id=organization_id,
            document_id=document.id,
            data=pdf_data,
        )
        update_document_status(db, document=document, status=DocumentStatus.PROCESSING)

        pages = extract_text_from_pdf(pdf_data)
        text_chunks = chunk_pages(pages)
        chunk_rows = bulk_create_chunks(db, document_id=document.id, chunks=text_chunks)
        try:
            embed_document_chunks(
                organization_id=organization_id,
                document=document,
                chunks=chunk_rows,
            )
        except EmbeddingError:
            db.execute(delete(Chunk).where(Chunk.document_id == document.id))
            db.flush()
            raise

        update_document_status(db, document=document, status=DocumentStatus.READY)
    except Exception:
        update_document_status(db, document=document, status=DocumentStatus.FAILED)
        db.commit()
        db.refresh(document)
        raise

    db.commit()
    db.refresh(document)
    return document
