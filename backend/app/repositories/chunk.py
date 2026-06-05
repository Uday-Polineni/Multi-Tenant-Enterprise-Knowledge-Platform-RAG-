import uuid

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.services.chunking import TextChunk


def bulk_create_chunks(
    db: Session,
    *,
    document_id: uuid.UUID,
    chunks: list[TextChunk],
) -> list[Chunk]:
    rows = [
        Chunk(
            document_id=document_id,
            chunk_index=chunk.chunk_index,
            page_number=chunk.page_number,
            section_name=chunk.section_name,
            content=chunk.content,
        )
        for chunk in chunks
    ]
    db.add_all(rows)
    db.flush()
    return rows
