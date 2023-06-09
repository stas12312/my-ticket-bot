"""add_indexes

Revision ID: 233c02159b55
Revises: f85775680fe6
Create Date: 2023-02-10 23:35:35.393944

"""
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '233c02159b55'
down_revision = 'f85775680fe6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('city_is_deleted_idx', 'city', ['is_deleted'])
    op.create_index('city_name_idx', 'city', [text('lower(name)')])

    op.create_index('location_city_id_idx', 'location', ['city_id'])
    op.create_index('location_name_idx', 'location', [text('lower(name)')])

    op.create_index('event_location_id_idx', 'event', ['location_id'])
    op.create_index('event_time_idx', 'event', ['time'])
    op.create_index('event_user_id_idx', 'event', ['user_id'])

    op.create_index('ticket_event_id_idx', 'ticket', ['event_id'])
    op.create_index('file_ticket_id_idx', 'file', ['ticket_id'])


def downgrade() -> None:
    op.drop_index('city_is_deleted_idx')
    op.drop_index('city_name_idx')

    op.drop_index('location_city_id_idx')
    op.drop_index('location_name_idx')

    op.drop_index('event_location_id_idx')
    op.drop_index('event_time_idx')
    op.drop_index('event_user_id_idx')

    op.drop_index('ticket_event_id_idx')
    op.drop_index('file_ticket_id_idx')
