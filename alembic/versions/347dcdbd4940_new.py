"""new

Revision ID: 347dcdbd4940
Revises: 11d21943f16f
Create Date: 2024-11-30 16:36:44.580114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '347dcdbd4940'
down_revision: Union[str, None] = '11d21943f16f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'family_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'family_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###