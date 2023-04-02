"""Конфигурация приложения"""
import dataclasses
import os
from enum import StrEnum


class EnvName(StrEnum):
    """Название переменных окружения"""
    BOT_TOKEN = 'BOT_TOKEN'
    ADMIN_IDS = 'ADMIN_IDS'
    LOGGING_LEVEL = 'LOGGING_LEVEL'

    PG_HOST = 'PG_HOST'
    PG_PORT = 'PG_PORT'
    PG_USER = 'PG_USER'
    PG_PASSWORD = 'PG_PASSWORD'
    PG_DB = 'PG_DB'

    HOST = 'HOST'


@dataclasses.dataclass
class Config:
    """Конфигурация приложения"""
    bot_token: str
    admin_ids: list[int]

    pg_host: str
    pg_port: int
    pg_user: str
    pg_password: str
    pg_db: str

    logging_level: str
    host: str

    def get_dsn(self) -> str:
        """Формирование DSN строки для postgres"""
        return f'postgres://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}'


def load_config() -> Config:
    """Загрузка конфигурации"""
    return Config(
        bot_token=os.environ.get(EnvName.BOT_TOKEN),
        admin_ids=[int(v) for v in os.environ.get(EnvName.ADMIN_IDS).split(',')],
        pg_host=os.environ.get(EnvName.PG_HOST),
        pg_port=int(os.environ.get(EnvName.PG_PORT)),
        pg_user=os.environ.get(EnvName.PG_USER),
        pg_password=os.environ.get(EnvName.PG_PASSWORD),
        pg_db=os.environ.get(EnvName.PG_DB),
        logging_level=os.environ.get(EnvName.LOGGING_LEVEL),
        host=os.environ.get(EnvName.HOST),
    )
