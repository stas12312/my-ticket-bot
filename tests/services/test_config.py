"""Тестирования конфигурации"""
import os

from services.config import EnvName, load_config


def setup():
    """Загрузка переменных в окружение"""
    os.environ.update({
        EnvName.BOT_TOKEN: 'bot_token',
        EnvName.ADMIN_ID: '111555',
        EnvName.PG_PORT: '5554',
        EnvName.PG_USER: 'postgres',
        EnvName.PG_PASSWORD: 'password',
        EnvName.PG_DB: 'db',
        EnvName.LOGGING_LEVEL: 'DEBUG',
    })


def test_load_config():
    """Тест загрузки конфигурации"""

    config = load_config()

    assert config.bot_token == 'bot_token'
    assert config.admin_id == 111555
    assert config.pg_port == 5554
    assert config.pg_user == 'postgres'
    assert config.pg_password == 'password'
    assert config.pg_db == 'db'
    assert config.logging_level == 'DEBUG'
