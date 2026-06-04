"""Add users table

Revision ID: 134458fc4b94
Revises: 3825ea8932f3
Create Date: 2026-05-18 16:47:43.217175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

# revision identifiers, used by Alembic.
revision: str = '134458fc4b94'
down_revision: Union[str, Sequence[str], None] = '3825ea8932f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users", 
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at",  TIMESTAMP(timezone=True), 
        nullable=False, server_default=text('now()')),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
