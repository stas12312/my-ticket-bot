from collections import defaultdict

import aiogram
import asyncpg

from bot.bulk_mailing import next_day_events_mailing


async def send_day_notifications(
        bot: aiogram.Bot,
        poll: asyncpg.Pool,
):
    """Ежедневная отправка уведомления о мероприятиях на следующей день"""
    connection: asyncpg.Connection
    async with poll.acquire() as connection:
        events = await connection.fetch(GET_USER_WITH_EVENT_FOR_NEXT_DAY)

        events_by_user = defaultdict(list)
        for event in events:
            events_by_user[event.get('user_id')].append(event.get('event_id'))
        await next_day_events_mailing(bot, events_by_user, connection)


GET_USER_WITH_EVENT_FOR_NEXT_DAY = """
    /*
    Получение городов, в которых по локальному времени переданное время
    */
    WITH city_with_12am AS (
        SELECT
            city.id,
            city.timezone
        FROM city
        WHERE
            EXTRACT(HOUR FROM now() AT TIME ZONE city.timezone) = 12
            AND city.is_deleted IS DISTINCT FROM TRUE
    )
    -- Выбираем события, которые будут "Завтра"
    SELECT
        event.id AS event_id,
        event.user_id AS user_id
    FROM event
    JOIN location ON location.id = event.location_id
    JOIN city_with_12am city ON city.id = location.city_id
    WHERE
        date(event.time AT TIME ZONE city.timezone) = date(now() AT TIME ZONE city.timezone) + interval '1 day'
        -- Нет смыслы учитывать прошедшие мероприятия и дальние мероприятия
        AND event.time > now() AND event.time < now() + interval '3 day'
"""
