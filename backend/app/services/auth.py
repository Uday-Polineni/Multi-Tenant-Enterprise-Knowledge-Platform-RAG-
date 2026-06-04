from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import UserRole
from app.repositories.organization import create_organization
from app.repositories.user import create_user, get_user_by_email
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class InvalidCredentialsError(Exception):
    pass


def register(db: Session, data: RegisterRequest) -> TokenResponse:
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

    access_token = create_access_token(
        user_id=str(user.id),
        organization_id=str(organization.id),
        role=user.role.value,
    )
    return TokenResponse(access_token=access_token)


def login(db: Session, data: LoginRequest) -> TokenResponse:
    user = get_user_by_email(db, data.email)
    if user is None or not verify_password(data.password, user.password_hash):
        raise InvalidCredentialsError("Invalid email or password")

    access_token = create_access_token(
        user_id=str(user.id),
        organization_id=str(user.organization_id),
        role=user.role.value,
    )
    return TokenResponse(access_token=access_token)
