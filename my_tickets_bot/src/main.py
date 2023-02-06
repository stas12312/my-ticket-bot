"""Настройка и запуск бота"""
import asyncio
import logging

import asyncpg
from aiogram import Dispatcher, Bot

from bot.commands import BOT_COMMANDS
from bot.handlers import main_router
from bot.middlewares import DbMiddleware
from services.config import load_config

config = load_config()

# Настройка логирования
logging.basicConfig(level=logging.getLevelName(config.logging_level))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def main():
    """Запуск бота"""
    poll = await asyncpg.create_pool(
        dsn=config.get_dsn(),
    )

    db_middleware = DbMiddleware(poll)

    dp = Dispatcher()
    dp.include_router(main_router)

    dp.update.outer_middleware.register(db_middleware)

    logger.info('Запуск бота')
    bot = Bot(config.bot_token, parse_mode='MarkdownV2')
    await bot.set_my_commands(BOT_COMMANDS)
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(main())
