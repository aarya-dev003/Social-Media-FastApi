"""Sync admin

Revision ID: 9ef8912e2e8b
Revises: 4305f5de0544
Create Date: 2024-11-06 19:28:56.807020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ef8912e2e8b'
down_revision: Union[str, None] = '4305f5de0544'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'admin', ['username'])
    op.create_unique_constraint(None, 'admin', ['email'])
    op.create_foreign_key(None, 'announcement', 'admin', ['admin_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'announcement', type_='foreignkey')
    op.drop_constraint(None, 'admin', type_='unique')
    op.drop_constraint(None, 'admin', type_='unique')
    # ### end Alembic commands ###