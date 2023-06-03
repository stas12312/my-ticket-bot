import datetime

from aiogram.utils.markdown import link, bold
from asyncpg import Record

from bot.emoji import get_clock_emoji
from services.event_time import get_beatify_datetime


def make_poster_event_message(
        event: Record,
) -> str:
    """Формирование сообщения для события парсера"""

    event_link = link(event.get('name'), event.get('url'))
    parser_datetime = datetime.datetime.fromisoformat(event.get('datetime'))
    return f'✨ *{event_link}*\n' \
           f'{get_clock_emoji(parser_datetime)} {bold(get_beatify_datetime(parser_datetime))}\n'
