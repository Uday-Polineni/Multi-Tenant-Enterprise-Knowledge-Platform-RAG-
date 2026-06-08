from app.models.document import DocumentAccessLevel
from app.models.user import UserRole

ROLE_ACCESS_LEVELS: dict[UserRole, frozenset[DocumentAccessLevel]] = {
    UserRole.ADMIN: frozenset(DocumentAccessLevel),
    UserRole.MANAGER: frozenset(
        {
            DocumentAccessLevel.PUBLIC,
            DocumentAccessLevel.HR,
            DocumentAccessLevel.ENGINEERING,
            DocumentAccessLevel.FINANCE,
        }
    ),
    UserRole.EMPLOYEE: frozenset({DocumentAccessLevel.PUBLIC}),
}


def allowed_levels_for_role(role: str | UserRole) -> list[str]:
    if isinstance(role, str):
        role = UserRole(role)
    return sorted(level.value for level in ROLE_ACCESS_LEVELS[role])


def can_access_level(role: str | UserRole, access_level: DocumentAccessLevel | str) -> bool:
    if isinstance(role, str):
        role = UserRole(role)
    if isinstance(access_level, str):
        access_level = DocumentAccessLevel(access_level)
    return access_level in ROLE_ACCESS_LEVELS[role]
