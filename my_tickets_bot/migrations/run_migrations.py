import os

from alembic import command
from alembic.config import Config


def run_migrations(script_location: str, dsn: str) -> None:
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')


def get_connection_url() -> str:
    """Получение URL для подключения к БД"""
    pg_user = os.environ.get('PG_USER')
    pg_password = os.environ.get('PG_PASSWORD')
    pg_host = os.environ.get('PG_HOST')
    pg_port = os.environ.get('PG_PORT')
    pg_db = os.environ.get('PG_DB')
    return f'postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'


if __name__ == '__main__':
    run_migrations('./my-tickets-bot', get_connection_url())
