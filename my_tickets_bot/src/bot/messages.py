"""Формирование красивых сообщений"""
import datetime

from aiogram.utils.markdown import bold, link, italic
from aiogram.utils.text_decorations import markdown_decoration as mark

from bot.emoji import get_clock_emoji
from models import Event, Location


def make_event_message(
        event: Event,
        with_command: bool = False,
) -> str:
    """Формирование сообщения для описания билета"""

    event_link = link(event.name, event.link)

    rows = [
        f'🎟 Билет на *{event_link}*',
        f'📍 {get_full_address_message(event.location)}',
        f'{get_clock_emoji(event.time)} {bold(beatify_date(event.time))}',
    ]

    if with_command:
        command = mark.quote(f'/event_{event.event_id}')
        rows.append(f'⚙ Управлять билетами: {command}')

    return '\n'.join(rows)


def get_full_address_message(
        location: Location,
) -> str:
    """Получение строки для адреса"""
    address = f'{mark.quote(location.city.name)}, {mark.quote(location.address)}'
    return f'{mark.bold(location.name)} ' \
           f'{italic(address)}'


def beatify_date(raw_datetime: datetime.datetime) -> str:
    """Преобразование даты в корректное представление"""

    return raw_datetime.strftime('%d.%m.%Y %H:%M')
