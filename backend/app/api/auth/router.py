from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.deps import CurrentUser, require_admin
from app.schemas.auth import (
    DemoCredentialsResponse,
    InviteRequest,
    InviteResponse,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
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
from app.services.refresh_token import (
    RefreshTokenError,
    RefreshTokenReuseError,
    logout_refresh_token,
    rotate_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/demo-credentials", response_model=DemoCredentialsResponse)
def get_demo_credentials() -> DemoCredentialsResponse:
    settings = get_settings()
    email = (settings.demo_admin_email or "").strip().lower()
    password = settings.demo_admin_password or ""
    if not email or not password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return DemoCredentialsResponse(email=email, password=password)


@router.post("/register", response_model=TokenResponse)
def register_user(
    data: RegisterRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    try:
        response = register(db, data)
        return response
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
        response = login(db, data)
        return response
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


@router.post("/refresh", response_model=TokenResponse)
def refresh_tokens(
    data: RefreshRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    try:
        response = rotate_refresh_token(db, raw_refresh_token=data.refresh_token)
        db.commit()
        return response
    except RefreshTokenReuseError as exc:
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
    except RefreshTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(
    data: LogoutRequest,
    db: Session = Depends(get_db),
) -> None:
    logout_refresh_token(db, raw_refresh_token=data.refresh_token)
    db.commit()


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
