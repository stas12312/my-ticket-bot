"""Массовые рассылки"""
import logging

import aiogram
import asyncpg

from bot.keybaords import get_actions_for_event
from bot.messages import make_event_message
from services.repositories import Repo

EVENTS_MAILING_TITLE = '❗ *Уведомление*❗\n_Напоминаем о ближайшем мероприятии_\n'
NEXT_DAY_MAILING_TITLE = '❗ *Уведомление*❗\n_Напоминаем о завтрашних мероприятиях_\n'

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
        event_msg = make_event_message(event)
        tickets = await repo.ticket.list_for_event(event.user.user_id, event.event_id)
        keyboard = get_actions_for_event(event, tickets)
        msg = f'{EVENTS_MAILING_TITLE}\n{event_msg}'
        await bot.send_message(
            chat_id=event.user.user_id,
            text=msg,
            reply_markup=keyboard,
        )


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
        await bot.send_message(
            chat_id=user_id,
            text=msg,
        )
