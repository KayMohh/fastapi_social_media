"""adding two more columns to posts table

Revision ID: bcb90cbdede6
Revises: 7f74dab97692
Create Date: 2024-11-21 10:19:57.968691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcb90cbdede6'
down_revision: Union[str, None] = '7f74dab97692'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
