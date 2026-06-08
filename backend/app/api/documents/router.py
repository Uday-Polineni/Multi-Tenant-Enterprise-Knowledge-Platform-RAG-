import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.access import can_access_level
from app.core.database import get_db
from app.core.deps import CurrentUser, get_current_user, require_admin
from app.core.storage import get_document_path, pdf_exists
from app.models.chunk import Chunk
from app.models.document import Document, DocumentAccessLevel, DocumentStatus
from app.repositories.document import get_document_by_id, list_documents_for_org
from app.schemas.document import DocumentListResponse, DocumentUploadResponse
from app.services.document import ingest_document, should_embed_async
from app.services.document_limits import PrototypeLimitError, validate_upload_limits
from app.services.document_embed import run_document_embedding
from app.services.document_lifecycle import DocumentNotFoundError, remove_document
from app.services.job_queue import enqueue_embed_document

router = APIRouter(prefix="/documents", tags=["documents"])


def _document_response(db: Session, document: Document) -> DocumentUploadResponse:
    chunk_count = db.scalar(
        select(func.count()).select_from(Chunk).where(Chunk.document_id == document.id)
    ) or 0
    return DocumentUploadResponse(
        id=document.id,
        filename=document.filename,
        status=document.status.value,
        access_level=document.access_level.value,
        organization_id=document.organization_id,
        chunk_count=chunk_count,
        created_at=document.created_at,
    )


@router.get("", response_model=DocumentListResponse)
def list_documents(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
) -> DocumentListResponse:
    documents = list_documents_for_org(
        db,
        organization_id=current_user.organization_id,
    )
    return DocumentListResponse(
        items=[_document_response(db, document) for document in documents]
    )


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    access_level: DocumentAccessLevel = Form(default=DocumentAccessLevel.PUBLIC),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
) -> DocumentUploadResponse:

    filename = file.filename or "document.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed",
        )

    pdf_data = await file.read()
    if not pdf_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file",
        )

    try:
        validate_upload_limits(
            db,
            organization_id=current_user.organization_id,
            filename=filename,
            pdf_data=pdf_data,
        )
        document = ingest_document(
            db,
            organization_id=current_user.organization_id,
            uploaded_by=current_user.id,
            filename=filename,
            pdf_data=pdf_data,
            access_level=access_level,
        )
    except PrototypeLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.detail,
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process document",
        ) from exc

    if document.status == DocumentStatus.PROCESSING and should_embed_async():
        queued = await enqueue_embed_document(
            document_id=document.id,
            organization_id=document.organization_id,
        )
        if not queued:
            try:
                run_document_embedding(
                    db,
                    document_id=document.id,
                    organization_id=document.organization_id,
                )
                db.commit()
                db.refresh(document)
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to index document",
                ) from exc

    return _document_response(db, document)


@router.get("/{document_id}/file")
def download_document_file(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> FileResponse:
    document = get_document_by_id(
        db,
        document_id=document_id,
        organization_id=current_user.organization_id,
    )
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    if not can_access_level(current_user.role, document.access_level):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this document",
        )
    if document.status != DocumentStatus.READY:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Document is not ready yet",
        )
    if not pdf_exists(
        organization_id=current_user.organization_id,
        document_id=document_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF file not found",
        )

    path = get_document_path(
        organization_id=current_user.organization_id,
        document_id=document_id,
    )
    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=document.filename,
        content_disposition_type="inline",
    )


@router.get("/{document_id}", response_model=DocumentUploadResponse)
def get_document_status(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
) -> DocumentUploadResponse:
    document = get_document_by_id(
        db,
        document_id=document_id,
        organization_id=current_user.organization_id,
    )
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return _document_response(db, document)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
) -> None:
    try:
        remove_document(
            db,
            organization_id=current_user.organization_id,
            document_id=document_id,
        )
        db.commit()
    except DocumentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        ) from exc
