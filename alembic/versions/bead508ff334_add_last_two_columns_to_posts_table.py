"""add last two columns to posts table

Revision ID: bead508ff334
Revises: 84a460727410
Create Date: 2026-05-18 17:46:23.334171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision: str = 'bead508ff334'
down_revision: Union[str, Sequence[str], None] = '84a460727410'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column('pubished', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column("posts", sa.Column('created_at', TIMESTAMP(timezone=True), 
        nullable=False, server_default=text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", 'published')
    op.drop_column("posts", 'created_at')
    
    pass
