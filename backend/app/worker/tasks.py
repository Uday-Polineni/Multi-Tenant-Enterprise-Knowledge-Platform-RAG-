import logging
import uuid

from app.core.database import SessionLocal
from app.services.document_embed import run_document_embedding
from app.services.embedding import EmbeddingError

logger = logging.getLogger(__name__)


async def embed_document_task(_ctx, document_id: str, organization_id: str) -> None:
    db = SessionLocal()
    try:
        run_document_embedding(
            db,
            document_id=uuid.UUID(document_id),
            organization_id=uuid.UUID(organization_id),
        )
        db.commit()
    except EmbeddingError:
        # run_document_embedding marks FAILED + removes chunks — persist that state
        db.commit()
        logger.exception(
            "Embed job failed for document %s org %s",
            document_id,
            organization_id,
        )
        raise
    except Exception:
        db.rollback()
        logger.exception(
            "Embed job failed for document %s org %s",
            document_id,
            organization_id,
        )
        raise
    finally:
        db.close()
