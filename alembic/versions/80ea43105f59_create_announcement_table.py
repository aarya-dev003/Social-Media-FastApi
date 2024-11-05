"""create announcement table

Revision ID: 80ea43105f59
Revises: 69ee483c02ce
Create Date: 2024-11-05 22:03:00.612154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP


# revision identifiers, used by Alembic.
revision: str = '80ea43105f59'
down_revision: Union[str, None] = '69ee483c02ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'announcement',
        sa.Column('id',sa.Integer(), primary_key = True, nullable = False),
        sa.Column('created_at', TIMESTAMP(timezone = True), nullable = False, server_default = sa.text('now()')),
        sa.Column('description', sa.String(), nullable= False),
        sa.Column('user_id', sa.Integer(), nullable=False)
        # sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete="CASCADE" )
    )


def downgrade() -> None:
    op.drop_table('announcement')
