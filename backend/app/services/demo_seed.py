"""Optional demo admin account for public portfolio deployments."""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.user import UserRole
from app.repositories.organization import create_organization
from app.repositories.user import create_user, get_user_by_email

logger = logging.getLogger(__name__)


def ensure_demo_admin(db: Session) -> None:
    settings = get_settings()
    email = (settings.demo_admin_email or "").strip().lower()
    password = settings.demo_admin_password or ""
    if not email or not password:
        return

    if get_user_by_email(db, email) is not None:
        return

    organization = create_organization(db, name=settings.demo_org_name)
    create_user(
        db,
        organization_id=organization.id,
        email=email,
        password_hash=hash_password(password),
        role=UserRole.ADMIN,
    )
    db.commit()
    logger.info("Demo admin account ready: %s", email)
