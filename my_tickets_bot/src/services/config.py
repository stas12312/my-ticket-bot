"""Конфигурация приложения"""
import dataclasses
import os
from enum import StrEnum


class EnvName(StrEnum):
    """Название переменных окружения"""
    BOT_TOKEN = 'BOT_TOKEN'
    ADMIN_ID = 'ADMIN_ID'
    LOGGING_LEVEL = 'LOGGING_LEVEL'

    PG_PORT = 'PG_PORT'
    PG_USER = 'PG_USER'
    PG_PASSWORD = 'PG_PASSWORD'
    PG_DB = 'PG_DB'


@dataclasses.dataclass
class Config:
    """Конфигурация приложения"""
    bot_token: str
    admin_id: int

    pg_port: int
    pg_user: str
    pg_password: str
    pg_db: str

    logging_level: str


def load_config() -> Config:
    """Загрузка конфигурации"""
    return Config(
        bot_token=os.environ.get(EnvName.BOT_TOKEN),
        admin_id=int(os.environ.get(EnvName.ADMIN_ID)),
        pg_port=int(os.environ.get(EnvName.PG_PORT)),
        pg_user=os.environ.get(EnvName.PG_USER),
        pg_password=os.environ.get(EnvName.PG_PASSWORD),
        pg_db=os.environ.get(EnvName.PG_DB),
        logging_level=os.environ.get(EnvName.LOGGING_LEVEL),
    )
