"""Настройка и запуск бота"""
import asyncio
import logging

import asyncpg
from aiogram import Dispatcher, Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.commands import BOT_COMMANDS
from bot.handlers import main_router
from bot.middlewares import DbMiddleware, ConfigMiddleware
from bot.utils import send_message_for_users
from parsers import PARSERS
from services.config import load_config
from services.notifications import send_notifications, send_day_notifications, send_new_events_notifications
from services.poster.poster import Poster

config = load_config()

# Настройка логирования
logging.basicConfig(level=logging.getLevelName(config.logging_level))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def start_scheduler(
        bot: Bot,
        poll: asyncpg.Pool,
):
    """Запуск планировщика"""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_notifications, 'cron', minute='*', args=(bot, poll))
    scheduler.add_job(send_day_notifications, 'cron', hour='*', args=(bot, poll))
    scheduler.add_job(send_new_events_notifications, 'cron', hour='*', args=(bot, poll))
    scheduler.start()


async def run_bot():
    """Запуск бота"""
    poll = await asyncpg.create_pool(
        dsn=config.get_dsn(),
    )
    # Регистрируем парсеры
    poster = Poster(poll=poll, parsers=PARSERS)
    await poster.register_parsers()

    db_middleware = DbMiddleware(poll)
    config_middleware = ConfigMiddleware(config)

    dispatcher = Dispatcher()
    dispatcher.include_router(main_router)

    dispatcher.update.outer_middleware.register(db_middleware)
    dispatcher.update.outer_middleware.register(config_middleware)

    logger.info('Запуск бота')
    bot = Bot(config.bot_token, parse_mode='MarkdownV2')

    await start_scheduler(bot, poll)
    await bot.set_my_commands(BOT_COMMANDS)
    await send_message_for_users(bot, config.admin_ids, '⚠️ ОБНОВЛЕНО ⚠️')
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(run_bot())
