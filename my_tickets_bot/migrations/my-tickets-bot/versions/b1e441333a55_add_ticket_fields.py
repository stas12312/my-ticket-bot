"""add ticket fields

Revision ID: b1e441333a55
Revises: cb210963c911
Create Date: 2023-02-05 17:41:32.340910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1e441333a55'
down_revision = 'cb210963c911'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'ticket',
        sa.Column('event_name', sa.String),
    )


def downgrade() -> None:
    op.drop_column('ticket', 'event_name')
