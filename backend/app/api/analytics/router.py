from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import CurrentUser, require_role
from app.repositories.query_log import list_query_logs
from app.schemas.query_log import QueryLogListResponse, QueryLogSummary

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/queries", response_model=QueryLogListResponse)
def list_recent_queries(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role("admin", "manager")),
) -> QueryLogListResponse:
    rows = list_query_logs(
        db,
        organization_id=current_user.organization_id,
        limit=limit,
        offset=offset,
    )
    return QueryLogListResponse(
        items=[QueryLogSummary.model_validate(row) for row in rows],
        limit=limit,
        offset=offset,
    )
