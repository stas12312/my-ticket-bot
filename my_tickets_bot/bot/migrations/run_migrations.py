"""Запуск миграции"""
import os
from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations(script_location: str, dsn: str) -> None:
    """Запуск миграции"""
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')


def get_connection_url() -> str:
    """Получение строки подключения к БД"""
    pg_user = os.environ.get('PG_USER')
    pg_password = os.environ.get('PG_PASSWORD')
    pg_host = os.environ.get('PG_HOST')
    pg_port = os.environ.get('PG_PORT')
    pg_db = os.environ.get('PG_DB')
    return f'postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'


def get_test_connection_url() -> str:
    """Получение строки подключения к тестовой БД"""
    pg_user = os.environ.get('PG_USER')
    pg_password = os.environ.get('PG_PASSWORD')
    return f'postgresql+asyncpg://{pg_user}:{pg_password}@localhost:6432/test'


if __name__ == '__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))
    migrations_path = Path(current_path) / Path('my-tickets-bot')
    print(current_path)

    run_migrations(migrations_path.as_posix(), get_connection_url())
