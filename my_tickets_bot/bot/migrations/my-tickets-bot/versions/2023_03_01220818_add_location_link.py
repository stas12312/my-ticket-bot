"""add location_link

Revision ID: 70ad93fe7ea2
Revises: 69573da1ab17
Create Date: 2023-03-01 22:08:18.063072

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '70ad93fe7ea2'
down_revision = '69573da1ab17'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('location', sa.Column('url', sa.String, nullable=True))
    op.create_index('location_url_idx', 'location', ['url'])


def downgrade() -> None:
    op.drop_column('location', 'url')
    op.drop_index('location_url_idx')
