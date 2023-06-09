"""add parser table

Revision ID: 22c55b11fb59
Revises: 9de1ce5f402d
Create Date: 2023-04-15 00:15:00.180530

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '22c55b11fb59'
down_revision = '9de1ce5f402d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'parser',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('name', sa.TEXT),
        sa.Column('url', sa.TEXT, unique=True),
        sa.Column('timezone', sa.TEXT),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('events', JSONB, nullable=True),
    )
    op.create_index('parser_url_idx', 'parser', ['url'])


def downgrade() -> None:
    op.drop_table('parser')
    op.drop_index('parser_url_idx')
