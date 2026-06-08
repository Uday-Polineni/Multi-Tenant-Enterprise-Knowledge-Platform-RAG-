"""Prototype upload limits — page count and documents per organization."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.document import count_documents_for_org, get_document_by_filename
from app.services.pdf_extract import count_pdf_pages


class PrototypeLimitError(Exception):
    """Raised when an upload violates prototype size or quota limits."""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


def validate_upload_limits(
    db: Session,
    *,
    organization_id: uuid.UUID,
    filename: str,
    pdf_data: bytes,
) -> None:
    settings = get_settings()

    if settings.prototype_max_pdf_pages > 0:
        page_count = count_pdf_pages(pdf_data)
        if page_count > settings.prototype_max_pdf_pages:
            raise PrototypeLimitError(
                f"This prototype only supports PDFs up to "
                f"{settings.prototype_max_pdf_pages} pages. Your file has {page_count} pages. "
                "Please upload a shorter document or split the file."
            )

    if settings.prototype_max_documents_per_org > 0:
        replacing = get_document_by_filename(
            db,
            organization_id=organization_id,
            filename=filename,
        )
        if replacing is None:
            document_count = count_documents_for_org(
                db,
                organization_id=organization_id,
            )
            if document_count >= settings.prototype_max_documents_per_org:
                raise PrototypeLimitError(
                    f"This prototype allows up to "
                    f"{settings.prototype_max_documents_per_org} documents per organization. "
                    f"You already have {document_count}. Delete an existing document before "
                    "uploading a new one."
                )
