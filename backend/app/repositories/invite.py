import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.invite import Invite
from app.models.user import UserRole


def create_invite(
    db: Session,
    *,
    organization_id: uuid.UUID,
    email: str,
    role: UserRole,
    token: str,
    expires_at: datetime,
) -> Invite:
    invite = Invite(
        organization_id=organization_id,
        email=email.lower(),
        role=role,
        token=token,
        expires_at=expires_at,
    )
    db.add(invite)
    db.flush()
    return invite


def get_invite_by_token(db: Session, token: str) -> Invite | None:
    stmt = select(Invite).where(Invite.token == token)
    return db.scalars(stmt).first()


def mark_invite_used(db: Session, *, invite: Invite) -> Invite:
    invite.used_at = datetime.now(timezone.utc)
    db.flush()
    return invite
