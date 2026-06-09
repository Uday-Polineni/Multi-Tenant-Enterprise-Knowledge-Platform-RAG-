import logging
import uuid
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.errors import InternalError as ChromaInternalError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus

logger = logging.getLogger(__name__)


class VectorIndexCorruptedError(Exception):
    """Chroma index is inconsistent and must be repaired from Postgres."""


@dataclass
class ChunkSearchResult:
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    filename: str
    page_number: int | None
    section_name: str | None
    content: str
    distance: float | None


def org_collection_name(organization_id: uuid.UUID) -> str:
    return f"org_{organization_id}"


@lru_cache
def get_chroma_client() -> chromadb.ClientAPI:
    settings = get_settings()
    persist_dir = Path(settings.chroma_persist_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_dir))


def get_org_collection(organization_id: uuid.UUID) -> Collection:
    client = get_chroma_client()
    name = org_collection_name(organization_id)
    return client.get_or_create_collection(
        name=name,
        metadata={"organization_id": str(organization_id)},
    )


def reset_org_collection(organization_id: uuid.UUID) -> Collection:
    """Drop and recreate the org collection to clear a corrupted vector index."""
    client = get_chroma_client()
    name = org_collection_name(organization_id)
    try:
        client.delete_collection(name)
        logger.info("Reset Chroma collection %s", name)
    except Exception:
        logger.debug("Chroma collection %s did not exist or could not be deleted", name)
    return client.get_or_create_collection(
        name=name,
        metadata={"organization_id": str(organization_id)},
    )


def _chunk_metadata(
    *,
    organization_id: uuid.UUID,
    document_id: uuid.UUID,
    chunk_id: uuid.UUID,
    filename: str,
    access_level: str,
    page_number: int | None,
    section_name: str | None,
) -> dict[str, str | int]:
    metadata: dict[str, str | int] = {
        "organization_id": str(organization_id),
        "document_id": str(document_id),
        "chunk_id": str(chunk_id),
        "filename": filename,
        "access_level": access_level,
    }
    if page_number is not None:
        metadata["page_number"] = page_number
    if section_name:
        metadata["section_name"] = section_name
    return metadata


def _chroma_ids_for_document(
    collection: Collection,
    document_id: uuid.UUID,
) -> list[str]:
    try:
        result = collection.get(
            where={"document_id": str(document_id)},
            include=[],
        )
        return list(result.get("ids") or [])
    except Exception:
        logger.exception("Failed to list Chroma ids for document %s", document_id)
        return []


def _valid_chunk_ids_for_org(db: Session, *, organization_id: uuid.UUID) -> set[str]:
    rows = db.scalars(
        select(Chunk.id)
        .join(Document, Chunk.document_id == Document.id)
        .where(Document.organization_id == organization_id)
    ).all()
    return {str(row) for row in rows}


def prune_orphan_vectors(db: Session, *, organization_id: uuid.UUID) -> int:
    """Remove Chroma vectors whose chunk ids no longer exist in Postgres."""
    collection = get_org_collection(organization_id)
    if collection.count() == 0:
        return 0

    try:
        stored = collection.get(include=[])
    except ChromaInternalError:
        logger.warning(
            "Chroma unreadable during orphan prune for org %s; skipping prune",
            organization_id,
        )
        return 0

    chroma_ids = set(stored.get("ids") or [])
    if not chroma_ids:
        return 0

    valid_ids = _valid_chunk_ids_for_org(db, organization_id=organization_id)
    orphan_ids = sorted(chroma_ids - valid_ids)
    if not orphan_ids:
        return 0

    collection.delete(ids=orphan_ids)
    logger.info(
        "Pruned %d orphan Chroma vector(s) for org %s",
        len(orphan_ids),
        organization_id,
    )
    return len(orphan_ids)


def rebuild_org_vector_index(db: Session, *, organization_id: uuid.UUID) -> None:
    """Rebuild the org vector index from Postgres (source of truth)."""
    from app.services.embedding import embed_document_chunks

    reset_org_collection(organization_id)

    documents = list(
        db.scalars(
            select(Document).where(
                Document.organization_id == organization_id,
                Document.status == DocumentStatus.READY,
            )
        ).all()
    )

    for document in documents:
        chunks = list(
            db.scalars(select(Chunk).where(Chunk.document_id == document.id)).all()
        )
        if not chunks:
            continue
        embed_document_chunks(
            organization_id=organization_id,
            document=document,
            chunks=chunks,
        )

    prune_orphan_vectors(db, organization_id=organization_id)
    logger.info(
        "Rebuilt Chroma index for org %s from %d ready document(s)",
        organization_id,
        len(documents),
    )


def verify_org_vector_index(
    db: Session,
    *,
    organization_id: uuid.UUID,
    probe_embedding: list[float],
) -> None:
    """Probe Chroma after writes; rebuild automatically if the index is corrupt."""
    collection = get_org_collection(organization_id)
    if collection.count() == 0:
        return

    try:
        collection.query(
            query_embeddings=[probe_embedding],
            n_results=1,
            include=["documents"],
        )
    except ChromaInternalError as exc:
        logger.warning(
            "Chroma probe failed for org %s; rebuilding vector index",
            organization_id,
        )
        rebuild_org_vector_index(db, organization_id=organization_id)


def upsert_chunks(
    *,
    organization_id: uuid.UUID,
    filename: str,
    access_level: str,
    chunks: list[Chunk],
    embeddings: list[list[float]],
) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")
    if not chunks:
        return

    collection = get_org_collection(organization_id)
    ids = [str(chunk.id) for chunk in chunks]
    documents = [chunk.content for chunk in chunks]
    metadatas = [
        _chunk_metadata(
            organization_id=organization_id,
            document_id=chunk.document_id,
            chunk_id=chunk.id,
            filename=filename,
            access_level=access_level,
            page_number=chunk.page_number,
            section_name=chunk.section_name,
        )
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def update_document_access_level_in_index(
    *,
    organization_id: uuid.UUID,
    document: Document,
    chunks: list[Chunk],
    access_level: str,
) -> None:
    """Patch access_level metadata on existing Chroma vectors for a document."""
    if not chunks:
        return

    collection = get_org_collection(organization_id)
    if collection.count() == 0:
        return

    indexed_ids = set(_chroma_ids_for_document(collection, document.id))
    if not indexed_ids:
        return

    ids: list[str] = []
    metadatas: list[dict[str, str | int]] = []
    for chunk in chunks:
        chunk_id = str(chunk.id)
        if chunk_id not in indexed_ids:
            continue
        ids.append(chunk_id)
        metadatas.append(
            _chunk_metadata(
                organization_id=organization_id,
                document_id=chunk.document_id,
                chunk_id=chunk.id,
                filename=document.filename,
                access_level=access_level,
                page_number=chunk.page_number,
                section_name=chunk.section_name,
            )
        )

    if not ids:
        return

    try:
        collection.update(ids=ids, metadatas=metadatas)
    except Exception:
        logger.exception(
            "Failed to update Chroma access_level for document %s in org %s",
            document.id,
            organization_id,
        )


def delete_chunks_for_document(
    *,
    organization_id: uuid.UUID,
    document_id: uuid.UUID,
    chunk_ids: list[uuid.UUID] | None = None,
) -> None:
    collection = get_org_collection(organization_id)
    if collection.count() == 0:
        return

    ids_to_delete = set(_chroma_ids_for_document(collection, document_id))
    ids_to_delete.update(str(chunk_id) for chunk_id in chunk_ids or [])

    try:
        if ids_to_delete:
            collection.delete(ids=sorted(ids_to_delete))
        collection.delete(where={"document_id": str(document_id)})
    except Exception:
        logger.exception(
            "Failed to delete Chroma chunks for document %s in org %s",
            document_id,
            organization_id,
        )


def _build_chroma_where(
    *,
    allowed_access_levels: list[str] | None,
    document_ids: list[uuid.UUID] | None = None,
    page_number: int | None = None,
) -> dict | None:
    clauses: list[dict] = []
    if allowed_access_levels is not None:
        if not allowed_access_levels:
            return {}
        clauses.append({"access_level": {"$in": allowed_access_levels}})
    if document_ids:
        id_strs = [str(document_id) for document_id in document_ids]
        if len(id_strs) == 1:
            clauses.append({"document_id": id_strs[0]})
        else:
            clauses.append({"document_id": {"$in": id_strs}})
    if page_number is not None:
        clauses.append({"page_number": page_number})

    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


def search(
    *,
    organization_id: uuid.UUID,
    query_embedding: list[float],
    top_k: int = 5,
    allowed_access_levels: list[str] | None = None,
    document_ids: list[uuid.UUID] | None = None,
    page_number: int | None = None,
) -> list[ChunkSearchResult]:
    collection = get_org_collection(organization_id)
    count = collection.count()
    if count == 0:
        return []

    where = _build_chroma_where(
        allowed_access_levels=allowed_access_levels,
        document_ids=document_ids,
        page_number=page_number,
    )
    if where == {}:
        return []

    try:
        response = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, count),
            where=where,
            include=["documents", "metadatas", "distances"],
        )
    except ChromaInternalError as exc:
        raise VectorIndexCorruptedError(
            "Chroma vector search failed; index must be rebuilt from Postgres"
        ) from exc

    ids = response.get("ids", [[]])[0]
    documents = response.get("documents", [[]])[0]
    metadatas = response.get("metadatas", [[]])[0]
    distances = response.get("distances", [[]])[0]

    results: list[ChunkSearchResult] = []
    for index, chunk_id in enumerate(ids):
        metadata = metadatas[index] or {}
        page_number = metadata.get("page_number")
        results.append(
            ChunkSearchResult(
                chunk_id=uuid.UUID(chunk_id),
                document_id=uuid.UUID(str(metadata["document_id"])),
                filename=str(metadata["filename"]),
                page_number=int(page_number) if page_number is not None else None,
                section_name=metadata.get("section_name") or None,
                content=documents[index] or "",
                distance=distances[index] if index < len(distances) else None,
            )
        )
    return results
