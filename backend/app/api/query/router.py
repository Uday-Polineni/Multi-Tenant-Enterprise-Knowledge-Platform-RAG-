from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import CurrentUser, get_current_user
from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag import answer_question

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
async def query_knowledge(
    body: QueryRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> QueryResponse:
    try:
        return answer_question(
            organization_id=current_user.organization_id,
            question=body.question,
            role=current_user.role,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to answer question",
        ) from exc
