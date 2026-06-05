import uuid

from app.core.ai.openai_embedding import get_embedding_provider
from app.models.chunk import Chunk
from app.models.document import Document
from app.services.vector_store import upsert_chunks


class EmbeddingError(Exception):
    """Embedding or Chroma upsert failed."""


def embed_document_chunks(
    *,
    organization_id: uuid.UUID,
    document: Document,
    chunks: list[Chunk],
) -> None:
    if not chunks:
        return

    try:
        embeddings = get_embedding_provider().embed_batch(
            [chunk.content for chunk in chunks]
        )
        upsert_chunks(
            organization_id=organization_id,
            filename=document.filename,
            chunks=chunks,
            embeddings=embeddings,
        )
    except Exception as exc:
        raise EmbeddingError("Failed to embed document chunks") from exc
