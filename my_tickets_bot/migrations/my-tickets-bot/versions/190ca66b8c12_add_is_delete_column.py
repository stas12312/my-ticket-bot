"""add is_delete column

Revision ID: 190ca66b8c12
Revises: 5329f1b9835c
Create Date: 2023-02-05 02:14:41.199524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '190ca66b8c12'
down_revision = '5329f1b9835c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'city',
        sa.Column('is_deleted', sa.BOOLEAN, nullable=True),
    )
    op.add_column(
        'place',
        sa.Column('is_deleted', sa.BOOLEAN, nullable=True),
    )


def downgrade() -> None:
    op.drop_column('city', 'is_deleted')
    op.drop_column('place', 'is_deleted')
