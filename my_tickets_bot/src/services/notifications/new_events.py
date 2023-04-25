import dataclasses
import datetime
import logging

import aiogram
import asyncpg
import pytz
from aiogram.utils.markdown import link, bold

from bot.emoji import get_clock_emoji
from bot.utils import safe_send_message
from parsers import PARSERS
from services.event_time import get_beatify_datetime
from services.poster import Event
from services.poster.poster import Poster, ParserResult

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclasses.dataclass
class UserLocation:
    """Локация пользователя"""
    user_id: int
    location_name: str


async def send_new_events_notifications(
        bot: aiogram.Bot,
        pool: asyncpg.Pool,
):
    """Отправка уведомлений """
    poster = Poster(pool, PARSERS, bot)
    parsers_events = await poster.get_parsers_events(datetime.datetime.now(pytz.utc))
    async with pool.acquire() as conn:
        await send_by_parsers(conn, bot, parsers_events)


async def send_by_parsers(
        conn: asyncpg.Connection,
        bot: aiogram.Bot,
        parsers_with_events: list[ParserResult],
) -> None:
    """Отправка уведомлений для парсеров"""
    for parser_events in parsers_with_events:
        url = parser_events.parser.config.url
        users = await get_user_ids_by_location_url(conn, url)
        logger.info('Пользователи для парсера %s: %s', parser_events.parser.name, str(users))
        await send_for_users(bot, users, parser_events.events)


def make_message(
        location_name: str,
        events: list[Event],
) -> str:
    """Формирование сообщения для уведомления"""
    title = f'Новые мероприятия в {location_name}'
    rows = [
        title,
    ]
    for event in events:
        event_link = link(event.name, event.url)
        rows.extend([
            f'✨ *{event_link}*',
            f'{get_clock_emoji(event.datetime)} {bold(get_beatify_datetime(event.datetime))}\n'
        ])

    return '\n'.join(rows)


async def send_for_users(
        bot: aiogram.Bot,
        users: list[UserLocation],
        events: list[Event],
) -> None:
    """Отправка уведомления"""
    for user in users:
        msg = make_message(user.location_name, events)
        await safe_send_message(bot, user.user_id, msg, disable_web_page_preview=True)


async def get_user_ids_by_location_url(
        conn: asyncpg.Connection,
        url: str,
) -> list[UserLocation]:
    """Получение идентификаторов пользователей по URL места проведения"""
    users_with_location = await conn.fetch(GET_USERS_BY_LOCATION_URL, url)
    return [UserLocation(user.get('id'), user.get('name')) for user in users_with_location]


GET_USERS_BY_LOCATION_URL = """
    SELECT 
        "user".id, 
        location.name
    FROM location
    JOIN city ON city.id = location.city_id
    JOIN "user" ON "user".id = city.user_id
    WHERE 
        location.url = $1
        AND location.is_deleted IS DISTINCT FROM TRUE
        AND city.is_deleted IS DISTINCT FROM TRUE
"""
