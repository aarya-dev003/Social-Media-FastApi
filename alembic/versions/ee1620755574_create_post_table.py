"""Create Post Table

Revision ID: ee1620755574
Revises: f9b7ff9f82e9
Create Date: 2024-10-25 13:20:04.146294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP


# revision identifiers, used by Alembic.
revision: str = 'ee1620755574'
down_revision: Union[str, None] = 'f9b7ff9f82e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table(
        'post',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, server_default='True', nullable=False),
        sa.Column('created_at', TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
         )


def downgrade() -> None:
    op.drop_table('post')
