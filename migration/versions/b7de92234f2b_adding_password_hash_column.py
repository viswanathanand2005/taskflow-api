"""adding password_hash column

Revision ID: b7de92234f2b
Revises: 57263d950d90
Create Date: 2026-02-10 09:04:36.921796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7de92234f2b'
down_revision: Union[str, Sequence[str], None] = '57263d950d90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(table_name='users',column=sa.Column('password_hash',sa.VARCHAR(length=255),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','password_hash')
    pass
