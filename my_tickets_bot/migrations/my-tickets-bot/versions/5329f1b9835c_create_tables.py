"""create tables

Revision ID: 5329f1b9835c
Revises: 
Create Date: 2023-02-04 20:26:53.649429

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5329f1b9835c'
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
    )

    op.create_table(
        'place',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('city_id', sa.BIGINT, sa.ForeignKey('city.id')),
    )

    op.create_table(
        'file',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('location', sa.String),
        sa.Column('type', sa.INT),
    )

    op.create_table(
        'ticket',
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('event_time', sa.DateTime(timezone=True)),
        sa.Column('user_id', sa.BIGINT, sa.ForeignKey('user.id')),
        sa.Column('place_id', sa.BIGINT, sa.ForeignKey('place.id')),
        sa.Column('event_link', sa.String, nullable=True),
        sa.Column('file_id', sa.BIGINT, sa.ForeignKey('file.id'), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('user')
    op.drop_table('city')
    op.drop_table('file')
    op.drop_table('place')
    op.drop_table('ticket')
