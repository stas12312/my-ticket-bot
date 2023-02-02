"""Настройка и запуск бота"""
import logging

from aiogram import Dispatcher, Bot

from services.config import load_config

config = load_config()

# Настройка логирования
logging.basicConfig(level=logging.getLevelName(config.logging_level))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dp = Dispatcher()


def main():
    """Запуск бота"""
    bot = Bot(config.bot_token)
    logger.debug('Запуск бота')
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
