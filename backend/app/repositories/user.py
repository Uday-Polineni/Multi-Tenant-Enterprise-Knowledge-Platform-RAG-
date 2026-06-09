import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User, UserRole


def create_user(
    db: Session,
    *,
    organization_id: uuid.UUID,
    email: str,
    password_hash: str,
    role: UserRole,
) -> User:
    user = User(
        organization_id=organization_id,
        email=email,
        password_hash=password_hash,
        role=role,
    )
    db.add(user)
    db.flush()
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()


def get_user_by_id(db: Session, *, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)
