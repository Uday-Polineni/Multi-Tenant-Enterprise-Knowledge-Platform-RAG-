import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.core.deps import CurrentUser, get_current_user
from app.core.rate_limit import RateLimitExceeded, check_rate_limit
from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag import answer_question, stream_answer_question

router = APIRouter(prefix="/query", tags=["query"])
logger = logging.getLogger(__name__)


@router.post("", response_model=QueryResponse)
async def query_knowledge(
    body: QueryRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> QueryResponse:
    try:
        check_rate_limit(
            organization_id=current_user.organization_id,
            user_id=current_user.id,
        )
    except RateLimitExceeded as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc

    try:
        return answer_question(
            db=db,
            organization_id=current_user.organization_id,
            user_id=current_user.id,
            question=body.question,
            role=current_user.role,
        )
    except Exception as exc:
        logger.exception("Query failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc) or exc.__class__.__name__,
        ) from exc


@router.post("/stream")
async def query_knowledge_stream(
    body: QueryRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> StreamingResponse:
    try:
        check_rate_limit(
            organization_id=current_user.organization_id,
            user_id=current_user.id,
        )
    except RateLimitExceeded as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc

    def event_generator():
        import json

        db = SessionLocal()
        try:
            yield from stream_answer_question(
                db=db,
                organization_id=current_user.organization_id,
                user_id=current_user.id,
                question=body.question,
                role=current_user.role,
            )
        except Exception as exc:
            logger.exception("Stream query failed")
            detail = str(exc) or exc.__class__.__name__
            yield f"event: error\ndata: {json.dumps({'detail': detail})}\n\n"
        finally:
            db.close()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
