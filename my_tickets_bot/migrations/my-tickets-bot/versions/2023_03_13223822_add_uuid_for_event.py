"""add uuid for event

Revision ID: 19894e7e5434
Revises: 70ad93fe7ea2
Create Date: 2023-03-13 22:38:22.251093

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '19894e7e5434'
down_revision = '70ad93fe7ea2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('event', sa.Column(
        'UUID', sa.UUID(as_uuid=True),
        index=True,
        nullable=True,
        server_default=sa.func.gen_random_uuid(),
        unique=True,
    ))


def downgrade() -> None:
    op.drop_column('event', 'UUID')
