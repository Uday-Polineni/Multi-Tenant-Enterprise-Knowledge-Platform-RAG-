from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import CurrentUser, require_admin
from app.models.chunk import Chunk
from app.models.document import DocumentAccessLevel
from app.schemas.document import DocumentUploadResponse
from app.services.document import ingest_document

router = APIRouter(prefix="/documents", tags=["documents"])


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
        document = ingest_document(
            db,
            organization_id=current_user.organization_id,
            uploaded_by=current_user.id,
            filename=filename,
            pdf_data=pdf_data,
            access_level=access_level,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process document",
        ) from exc

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
