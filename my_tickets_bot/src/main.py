"""Настройка и запуск бота"""
import asyncio
import logging

import asyncpg
from aiogram import Dispatcher, Bot

from services.config import load_config

config = load_config()

# Настройка логирования
logging.basicConfig(level=logging.getLevelName(config.logging_level))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dp = Dispatcher()


async def main():
    """Запуск бота"""
    poll = await asyncpg.create_pool(
        dsn=config.get_dsn(),
    )

    async with poll.acquire() as connection:
        async with connection.transaction():
            print(await connection.fetchval('SELECT TRUE'))

    bot = Bot(config.bot_token)
    logger.debug('Запуск бота')
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(main())
