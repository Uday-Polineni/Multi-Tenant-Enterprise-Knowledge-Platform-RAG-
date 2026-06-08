"""add chunk search_vector for hybrid FTS

Revision ID: b2f1a8c4e901
Revises: ac9f3cc95bd1
Create Date: 2026-06-08 18:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b2f1a8c4e901"
down_revision: Union[str, Sequence[str], None] = "ac9f3cc95bd1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "chunks",
        sa.Column("search_vector", postgresql.TSVECTOR(), nullable=True),
    )
    op.execute(
        """
        UPDATE chunks
        SET search_vector = to_tsvector(
            'english',
            coalesce(section_name, '') || ' ' || content
        )
        """
    )
    op.create_index(
        "ix_chunks_search_vector",
        "chunks",
        ["search_vector"],
        unique=False,
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("ix_chunks_search_vector", table_name="chunks")
    op.drop_column("chunks", "search_vector")
