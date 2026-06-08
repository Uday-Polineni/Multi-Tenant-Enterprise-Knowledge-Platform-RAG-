import uuid

from sqlalchemy import delete, func, select, text
from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import Document, DocumentAccessLevel
from app.services.chunking import TextChunk
from app.services.vector_store import ChunkSearchResult


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
    _refresh_chunk_search_vectors(db, document_id=document_id)
    return rows


def _refresh_chunk_search_vectors(db: Session, *, document_id: uuid.UUID) -> None:
    db.execute(
        text(
            """
            UPDATE chunks
            SET search_vector = to_tsvector(
                'english',
                coalesce(section_name, '') || ' ' || content
            )
            WHERE document_id = :document_id
            """
        ),
        {"document_id": document_id},
    )
    db.flush()


def delete_chunks_for_document(db: Session, *, document_id: uuid.UUID) -> None:
    db.execute(delete(Chunk).where(Chunk.document_id == document_id))
    db.flush()


def search_chunks_fulltext(
    db: Session,
    *,
    organization_id: uuid.UUID,
    question: str,
    allowed_access_levels: list[str],
    top_k: int,
) -> list[ChunkSearchResult]:
    if not allowed_access_levels or not question.strip():
        return []

    ts_query = func.plainto_tsquery("english", question)
    rank = func.ts_rank_cd(Chunk.search_vector, ts_query)

    access_levels = [DocumentAccessLevel(level) for level in allowed_access_levels]

    stmt = (
        select(
            Chunk.id,
            Chunk.document_id,
            Chunk.page_number,
            Chunk.section_name,
            Chunk.content,
            Document.filename,
            rank.label("rank"),
        )
        .join(Document, Chunk.document_id == Document.id)
        .where(
            Document.organization_id == organization_id,
            Document.access_level.in_(access_levels),
            Chunk.search_vector.is_not(None),
            Chunk.search_vector.op("@@")(ts_query),
        )
        .order_by(rank.desc())
        .limit(top_k)
    )

    rows = db.execute(stmt).all()
    results: list[ChunkSearchResult] = []
    for row in rows:
        results.append(
            ChunkSearchResult(
                chunk_id=row.id,
                document_id=row.document_id,
                filename=row.filename,
                page_number=row.page_number,
                section_name=row.section_name,
                content=row.content,
                distance=None,
            )
        )
    return results


def chunks_exist_for_org(
    db: Session,
    *,
    organization_id: uuid.UUID,
    chunk_ids: list[str],
) -> bool:
    if not chunk_ids:
        return True

    try:
        parsed_ids = [uuid.UUID(value) for value in chunk_ids]
    except ValueError:
        return False

    count = db.scalar(
        select(func.count())
        .select_from(Chunk)
        .join(Document, Chunk.document_id == Document.id)
        .where(
            Chunk.id.in_(parsed_ids),
            Document.organization_id == organization_id,
        )
    )
    return count == len(parsed_ids)
