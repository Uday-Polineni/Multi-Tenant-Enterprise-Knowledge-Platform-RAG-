from sqlalchemy.orm import Session

from app.models.organization import Organization


def create_organization(db: Session, *, name: str) -> Organization:
    organization = Organization(name=name)
    db.add(organization)
    db.flush()
    return organization
