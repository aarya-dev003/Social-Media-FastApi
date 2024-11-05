"""create feedback table

Revision ID: ffd07c07be9d
Revises: 80ea43105f59
Create Date: 2024-11-05 23:32:05.264087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffd07c07be9d'
down_revision: Union[str, None] = '80ea43105f59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('issue', sa.String, nullable=False),
        sa.Column('issue_to', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('feedback')
