"""Create User Table

Revision ID: f9b7ff9f82e9
Revises: 
Create Date: 2024-10-25 13:17:48.360339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP


# revision identifiers, used by Alembic.
revision: str = 'f9b7ff9f82e9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
      op.create_table(
        'users',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table('users')
