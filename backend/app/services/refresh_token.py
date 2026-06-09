import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.refresh_token import (
    create_refresh_token_record,
    get_refresh_token_by_hash,
    hash_refresh_token,
    revoke_all_refresh_tokens_for_user,
    revoke_refresh_token,
)
from app.core.security import create_access_token
from app.repositories.user import get_user_by_id
from app.schemas.auth import TokenResponse


class RefreshTokenError(Exception):
    pass


class RefreshTokenReuseError(RefreshTokenError):
    """Presented when a rotated refresh token is reused (possible theft)."""


def _access_token_for_user(user: User) -> str:
    return create_access_token(
        user_id=str(user.id),
        organization_id=str(user.organization_id),
        role=user.role.value,
    )


def issue_token_pair(db: Session, user: User) -> TokenResponse:
    _, raw_refresh = create_refresh_token_record(db, user_id=user.id)
    return TokenResponse(
        access_token=_access_token_for_user(user),
        refresh_token=raw_refresh,
    )


def rotate_refresh_token(db: Session, *, raw_refresh_token: str) -> TokenResponse:
    token_hash = hash_refresh_token(raw_refresh_token)
    record = get_refresh_token_by_hash(db, token_hash=token_hash)
    if record is None:
        raise RefreshTokenError("Invalid refresh token")

    now = datetime.now(timezone.utc)

    if record.revoked_at is not None:
        if record.replaced_by_id is not None:
            revoke_all_refresh_tokens_for_user(db, user_id=record.user_id)
            raise RefreshTokenReuseError("Refresh token reuse detected")
        raise RefreshTokenError("Refresh token has been revoked")

    if record.expires_at < now:
        revoke_refresh_token(db, record=record)
        raise RefreshTokenError("Refresh token has expired")

    user = get_user_by_id(db, user_id=record.user_id)
    if user is None:
        revoke_refresh_token(db, record=record)
        raise RefreshTokenError("User not found")

    new_record, new_raw = create_refresh_token_record(db, user_id=user.id)
    revoke_refresh_token(db, record=record, replaced_by_id=new_record.id)

    return TokenResponse(
        access_token=_access_token_for_user(user),
        refresh_token=new_raw,
    )


def logout_refresh_token(db: Session, *, raw_refresh_token: str) -> None:
    token_hash = hash_refresh_token(raw_refresh_token)
    record = get_refresh_token_by_hash(db, token_hash=token_hash)
    if record is None:
        return
    if record.revoked_at is None:
        revoke_refresh_token(db, record=record)
