"""add foreign key to post table

Revision ID: 8f69876289ab
Revises: ee1620755574
Create Date: 2024-10-25 13:26:56.769225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f69876289ab'
down_revision: Union[str, None] = 'ee1620755574'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'post',
        sa.Column('user_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'post_user_fkey', source_table='post', referent_table= 'users', 
        local_cols=['user_id'],remote_cols=['id'], ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fkey', table_name='post')
    op.drop_column('post', 'user_id')
