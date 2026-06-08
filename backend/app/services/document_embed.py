import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import DocumentStatus
from app.repositories.document import get_document_by_id, update_document_status
from app.services.cache import invalidate_org_answer_cache
from app.services.embedding import EmbeddingError, embed_document_chunks
from app.services.vector_store import (
    prune_orphan_vectors,
    verify_org_vector_index,
)


def run_document_embedding(
    db: Session,
    *,
    document_id: uuid.UUID,
    organization_id: uuid.UUID,
) -> None:
    document = get_document_by_id(
        db,
        document_id=document_id,
        organization_id=organization_id,
    )
    if document is None:
        raise ValueError(f"Document {document_id} not found")

    chunks = list(
        db.scalars(select(Chunk).where(Chunk.document_id == document_id)).all()
    )
    try:
        embeddings = embed_document_chunks(
            organization_id=organization_id,
            document=document,
            chunks=chunks,
        )
        prune_orphan_vectors(db, organization_id=organization_id)
        if embeddings:
            verify_org_vector_index(
                db,
                organization_id=organization_id,
                probe_embedding=embeddings[0],
            )
        update_document_status(db, document=document, status=DocumentStatus.READY)
        invalidate_org_answer_cache(organization_id=organization_id)
    except EmbeddingError:
        db.execute(delete(Chunk).where(Chunk.document_id == document.id))
        db.flush()
        update_document_status(db, document=document, status=DocumentStatus.FAILED)
        raise
