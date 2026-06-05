import uuid
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection

from app.core.config import get_settings
from app.models.chunk import Chunk


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


def _chunk_metadata(
    *,
    organization_id: uuid.UUID,
    document_id: uuid.UUID,
    chunk_id: uuid.UUID,
    filename: str,
    page_number: int | None,
    section_name: str | None,
) -> dict[str, str | int]:
    metadata: dict[str, str | int] = {
        "organization_id": str(organization_id),
        "document_id": str(document_id),
        "chunk_id": str(chunk_id),
        "filename": filename,
    }
    if page_number is not None:
        metadata["page_number"] = page_number
    if section_name:
        metadata["section_name"] = section_name
    return metadata


def upsert_chunks(
    *,
    organization_id: uuid.UUID,
    filename: str,
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


def search(
    *,
    organization_id: uuid.UUID,
    query_embedding: list[float],
    top_k: int = 5,
) -> list[ChunkSearchResult]:
    collection = get_org_collection(organization_id)
    count = collection.count()
    if count == 0:
        return []

    response = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"],
    )

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
