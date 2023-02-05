"""add adress field

Revision ID: cb210963c911
Revises: 190ca66b8c12
Create Date: 2023-02-05 12:10:37.518919

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'cb210963c911'
down_revision = '190ca66b8c12'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'place',
        sa.Column('address', sa.String, nullable=True),
    )


def downgrade() -> None:
    op.drop_column('place', 'address')
