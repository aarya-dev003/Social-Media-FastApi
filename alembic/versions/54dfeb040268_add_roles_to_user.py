"""add roles to user

Revision ID: 54dfeb040268
Revises: ffd07c07be9d
Create Date: 2024-11-06 02:42:24.254923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54dfeb040268'
down_revision: Union[str, None] = 'ffd07c07be9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(), nullable= False, server_default='user'))


def downgrade() -> None:
    op.drop_column('users', 'role')
