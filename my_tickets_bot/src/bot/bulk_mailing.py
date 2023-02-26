"""Массовые рассылки"""
import logging

import aiogram
import asyncpg
from aiogram.exceptions import TelegramForbiddenError

from bot.services.events.messages import make_event_message, send_event_card
from bot.utils import safe_send_message
from services.repositories import Repo

EVENTS_MAILING_TITLE = '🔔 _Напоминаем о ближайшем мероприятии_ 🔔\n'
NEXT_DAY_MAILING_TITLE = '🔔 _Напоминаем о завтрашних мероприятиях_ 🔔\n'

logger = logging.getLogger(__name__)


async def coming_events_mailing(
        bot: aiogram.Bot,
        event_ids: list[int],
        connection: asyncpg.Connection
):
    """Массовое информирование о ближайших мероприятиях"""
    repo = Repo(connection)
    events = await repo.event.list(event_ids=event_ids)

    for event in events:
        logger.info('Отправка уведомления user_id=%s event_id=%s', event.user.user_id, event.event_id)
        try:
            await send_event_card(bot, event.user.user_id, event.event_id, repo, EVENTS_MAILING_TITLE)
        except TelegramForbiddenError:
            logger.info('Ошибка при отправке уведомления user_id=%s', event.user.user_id)


async def next_day_events_mailing(
        bot: aiogram.Bot,
        events_by_user: dict[int, list[int]],
        connection: asyncpg.Connection,
):
    """Массовое информирование о мероприятиях на следующий день"""
    repo = Repo(connection)

    for user_id, event_ids in events_by_user.items():
        events = await repo.event.list(event_ids=event_ids)
        events_msg = '\n\n'.join([make_event_message(e, with_command=True) for e in events])
        msg = f'{NEXT_DAY_MAILING_TITLE}\n{events_msg}'
        await safe_send_message(bot, user_id, msg, disable_web_page_preview=True)
