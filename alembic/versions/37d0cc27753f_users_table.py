"""users table

Revision ID: 37d0cc27753f
Revises: 485ef3ca784c
Create Date: 2024-11-21 10:06:38.107495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37d0cc27753f'
down_revision: Union[str, None] = '485ef3ca784c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id',),
        sa.UniqueConstraint('email',),
    )


def downgrade() -> None:
    op.drop_table('users')

