"""add user_name

Revision ID: 69573da1ab17
Revises: 8406801d827f
Create Date: 2023-02-19 00:24:49.379111

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '69573da1ab17'
down_revision = '8406801d827f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('first_name', sa.String, nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'first_name')
    op.drop_column('user', 'last_name')
