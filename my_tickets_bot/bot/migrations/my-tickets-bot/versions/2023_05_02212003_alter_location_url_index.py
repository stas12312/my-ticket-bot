"""alter location url index

Revision ID: 8bbccdcf5700
Revises: 22c55b11fb59
Create Date: 2023-05-02 21:20:03.267883

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8bbccdcf5700'
down_revision = '22c55b11fb59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index('location_url_idx')
    op.create_index('location_url_idx', 'location', [sa.text('lower(url) text_pattern_ops')])


def downgrade() -> None:
    op.drop_index('location_url_idx')
    op.create_index('location_url_idx', 'location', ['url'])
