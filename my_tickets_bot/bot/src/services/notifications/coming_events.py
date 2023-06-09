import datetime
import logging

import aiogram
import asyncpg

from bot.bulk_mailing import coming_events_mailing

logger = logging.getLogger(__name__)


async def send_notifications(
        bot: aiogram.Bot,
        poll: asyncpg.Pool,
):
    """Отправка уведомлений о ближайших мероприятиях"""
    now = datetime.datetime.now(datetime.timezone.utc)
    now = now.replace(second=0, microsecond=0) + datetime.timedelta(hours=3)

    logger.info('[start] Рассылка сообщений, отметка времени: %s', now.isoformat())

    connection: asyncpg.Connection
    async with poll.acquire() as connection:
        event_ids = await connection.fetchval(GET_TICKET_IDS_FOR_TIME, now)

        if event_ids:
            await coming_events_mailing(bot, event_ids, connection)

    logger.info('Найденные события: %s', event_ids)
    logger.info('[end] Рассылка сообщений')


GET_TICKET_IDS_FOR_TIME = """
    SELECT
        COALESCE(array_agg(event.id), '{}'::bigint[])
    FROM event
    WHERE 
        event.time = $1
"""
