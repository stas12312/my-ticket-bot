"""add end_time for event

Revision ID: 9de1ce5f402d
Revises: 19894e7e5434
Create Date: 2023-04-01 00:40:02.295551

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9de1ce5f402d'
down_revision = '19894e7e5434'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('event', sa.Column(
        'end_time', sa.DateTime(timezone=True),
        index=True,
        nullable=True,
    ))


def downgrade() -> None:
    op.drop_column('event', 'end_time')
