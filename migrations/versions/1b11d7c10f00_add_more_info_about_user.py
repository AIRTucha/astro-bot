"""add more info about user

Revision ID: 1b11d7c10f00
Revises: a1f3e055e849
Create Date: 2024-08-03 00:19:06.202649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b11d7c10f00'
down_revision: Union[str, None] = 'a1f3e055e849'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('target_topics', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('hobbies', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('self_description', sa.Text(), nullable=True))
    op.alter_column('users', 'language',
               existing_type=sa.VARCHAR(length=2),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'language',
               existing_type=sa.VARCHAR(length=2),
               nullable=False)
    op.drop_column('users', 'self_description')
    op.drop_column('users', 'hobbies')
    op.drop_column('users', 'target_topics')
    # ### end Alembic commands ###
