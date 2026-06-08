from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import CurrentUser, require_admin
from app.schemas.auth import (
    InviteRequest,
    InviteResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.services.auth import (
    InvalidCredentialsError,
    InviteError,
    PublicRegistrationDisabledError,
    create_invite_for_org,
    login,
    register,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register_user(
    data: RegisterRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    try:
        return register(db, data)
    except PublicRegistrationDisabledError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except InviteError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/login", response_model=TokenResponse)
def login_user(
    data: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    try:
        return login(db, data)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


@router.post("/invite", response_model=InviteResponse)
def invite_user(
    data: InviteRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
) -> InviteResponse:
    try:
        return create_invite_for_org(
            db,
            organization_id=current_user.organization_id,
            data=data,
        )
    except InviteError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
