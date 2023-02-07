"""init

Revision ID: f85775680fe6
Revises: b1e441333a55
Create Date: 2023-02-06 20:54:08.124292

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f85775680fe6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('username', sa.String, nullable=True),
    )

    op.create_table(
        'city',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('timezone', sa.String),
        sa.Column('user_id', sa.BIGINT, sa.ForeignKey('user.id')),
        sa.Column('is_deleted', sa.BOOLEAN, nullable=True),
    )

    # Таблица для места
    op.create_table(
        'location',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('city_id', sa.BIGINT, sa.ForeignKey('city.id')),
        sa.Column('address', sa.String, nullable=True),
        sa.Column('is_deleted', sa.BOOLEAN, nullable=True),
    )

    # Таблица для мероприятия
    op.create_table(
        'event',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('name', sa.String),
        sa.Column('link', sa.String, nullable=True),
        sa.Column('time', sa.DateTime(timezone=True)),
        sa.Column('location_id', sa.BIGINT, sa.ForeignKey('location.id')),
        sa.Column('user_id', sa.BIGINT, sa.ForeignKey('user.id')),
    )

    # Билет
    op.create_table(
        'ticket',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('event_id', sa.BIGINT, sa.ForeignKey('event.id', ondelete='CASCADE')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('comment', sa.String),
    )

    # Таблица для файла билета
    op.create_table(
        'file',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('location', sa.String, nullable=True),
        sa.Column('parent_id', sa.BIGINT, sa.ForeignKey('file.id', ondelete='CASCADE'), nullable=True),
        sa.Column('ticket_id', sa.BIGINT, sa.ForeignKey('ticket.id', ondelete='CASCADE')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('bot_file_id', sa.String, nullable=True)
    )

    def downgrade() -> None:
        op.drop_table('user')
        op.drop_table('city')
        op.drop_table('file')
        op.drop_table('place')
        op.drop_table('ticket')
        op.drop_table('event')
