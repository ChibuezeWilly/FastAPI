"""Add content column

Revision ID: 3825ea8932f3
Revises: 85ff83084f1d
Create Date: 2026-05-18 16:34:29.038545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3825ea8932f3'
down_revision: Union[str, Sequence[str], None] = '85ff83084f1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
