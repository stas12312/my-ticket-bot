"""add city_user_id_index

Revision ID: 8406801d827f
Revises: 233c02159b55
Create Date: 2023-02-12 20:45:27.763209

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '8406801d827f'
down_revision = '233c02159b55'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('city_name_user_id_idx', 'city', ['name', 'user_id'], unique=True)


def downgrade() -> None:
    op.drop_index('city_name_user_id_ids')
