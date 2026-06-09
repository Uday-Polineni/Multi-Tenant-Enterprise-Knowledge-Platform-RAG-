import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.refresh_token import RefreshToken


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def create_refresh_token_record(
    db: Session,
    *,
    user_id: uuid.UUID,
) -> tuple[RefreshToken, str]:
    settings = get_settings()
    raw_token = secrets.token_urlsafe(48)
    token_hash = hash_refresh_token(raw_token)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)

    record = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(record)
    db.flush()
    return record, raw_token


def get_refresh_token_by_hash(db: Session, *, token_hash: str) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    return db.scalars(stmt).first()


def revoke_refresh_token(
    db: Session,
    *,
    record: RefreshToken,
    replaced_by_id: uuid.UUID | None = None,
) -> None:
    now = datetime.now(timezone.utc)
    record.revoked_at = now
    if replaced_by_id is not None:
        record.replaced_by_id = replaced_by_id
    db.flush()


def revoke_all_refresh_tokens_for_user(db: Session, *, user_id: uuid.UUID) -> None:
    now = datetime.now(timezone.utc)
    db.execute(
        update(RefreshToken)
        .where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
        )
        .values(revoked_at=now)
    )
    db.flush()
