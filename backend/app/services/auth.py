import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories.invite import create_invite, get_invite_by_token, mark_invite_used
from app.repositories.organization import create_organization
from app.repositories.user import create_user, get_user_by_email
from app.schemas.auth import InviteRequest, InviteResponse, LoginRequest, RegisterRequest, TokenResponse


class InvalidCredentialsError(Exception):
    pass


class PublicRegistrationDisabledError(Exception):
    pass


class InviteError(Exception):
    pass


def register(db: Session, data: RegisterRequest) -> TokenResponse:
    if data.invite_token:
        return _register_with_invite(db, data)

    settings = get_settings()
    if not settings.allow_public_registration:
        raise PublicRegistrationDisabledError("Public registration is disabled")

    organization = create_organization(db, name=data.organization_name)
    user = create_user(
        db,
        organization_id=organization.id,
        email=data.email,
        password_hash=hash_password(data.password),
        role=UserRole.ADMIN,
    )
    db.commit()
    db.refresh(user)

    return _token_for_user(user)


def _register_with_invite(db: Session, data: RegisterRequest) -> TokenResponse:
    invite = get_invite_by_token(db, data.invite_token)
    if invite is None:
        raise InviteError("Invalid invite token")

    now = datetime.now(timezone.utc)
    if invite.used_at is not None:
        raise InviteError("Invite has already been used")
    if invite.expires_at < now:
        raise InviteError("Invite has expired")
    if invite.email.lower() != data.email.lower():
        raise InviteError("Email does not match invite")

    existing = db.scalars(
        select(User).where(
            User.organization_id == invite.organization_id,
            User.email == data.email.lower(),
        )
    ).first()
    if existing is not None:
        raise InviteError("User already exists in this organization")

    user = create_user(
        db,
        organization_id=invite.organization_id,
        email=data.email,
        password_hash=hash_password(data.password),
        role=invite.role,
    )
    mark_invite_used(db, invite=invite)
    db.commit()
    db.refresh(user)

    return _token_for_user(user)


def create_invite_for_org(
    db: Session,
    *,
    organization_id: uuid.UUID,
    data: InviteRequest,
) -> InviteResponse:
    existing = db.scalars(
        select(User).where(
            User.organization_id == organization_id,
            User.email == data.email.lower(),
        )
    ).first()
    if existing is not None:
        raise InviteError("User already exists in this organization")

    settings = get_settings()
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.invite_expire_days)

    invite = create_invite(
        db,
        organization_id=organization_id,
        email=data.email,
        role=data.role,
        token=token,
        expires_at=expires_at,
    )
    db.commit()
    db.refresh(invite)

    return InviteResponse(
        id=str(invite.id),
        email=invite.email,
        role=invite.role.value,
        token=invite.token,
        expires_at=invite.expires_at.isoformat(),
        organization_id=str(invite.organization_id),
    )


def login(db: Session, data: LoginRequest) -> TokenResponse:
    user = get_user_by_email(db, data.email)
    if user is None or not verify_password(data.password, user.password_hash):
        raise InvalidCredentialsError("Invalid email or password")

    return _token_for_user(user)


def _token_for_user(user: User) -> TokenResponse:
    access_token = create_access_token(
        user_id=str(user.id),
        organization_id=str(user.organization_id),
        role=user.role.value,
    )
    return TokenResponse(access_token=access_token)
