"""Формирование красивых сообщений"""
from datetime import datetime

import pytz
from aiogram.utils.markdown import bold, link, italic
from aiogram.utils.text_decorations import markdown_decoration

from bot.emoji import get_clock_emoji
from models import Event, Location, City
from services.event_time import get_beatify_datetime, get_left_time


def quote(
        value: str
) -> str:
    """Экранирование"""
    return markdown_decoration.quote(value)


def make_event_message(
        event: Event,
        with_command: bool = False,
) -> str:
    """Формирование сообщения для описания билета"""

    event_link = link(event.name, event.link)
    now = pytz.utc.localize(datetime.now()).astimezone(pytz.timezone(event.location.city.timezone))

    rows = [
        f'✨ *{event_link}*',
        f'🏛 {bold(event.location.name)}',
        f'📍 {get_address(event.location)}',
        f'{get_clock_emoji(event.time)} {bold(get_beatify_datetime(event.time))}',
    ]

    if left_time := get_left_time(now, event.time):
        rows.append(f'⏳ Через {italic(quote(left_time))}')

    if with_command:
        command = quote(f'/event_{event.event_id}')
        rows.append(f'⚙ Управлять {command}')

    return _make_message_by_rows(rows)


def get_full_address_message(
        location: Location,
) -> str:
    """Получение строки для адреса"""
    address = f'{quote(location.city.name)}, {quote(location.address)}'
    return f'{bold(location.name)} {italic(address)}'


def get_address(
        location: Location,
) -> str:
    """Получение адреса"""
    return f'{quote(location.city.name)}, {quote(location.address)}'


def make_city_message(
        city: City,
) -> str:
    """Формирование сообщения для описания города"""
    rows = [
        f'🏘 {quote(city.name)}',
        f'🕰 {quote(city.timezone)}',
    ]
    return _make_message_by_rows(rows)


def make_location_message(
        location: Location,
) -> str:
    """Формирования сообщения для локации"""
    rows = []

    if location.city.name:
        rows.append(
            f'🏘 {quote(location.city.name)}'
        )

    rows.extend([
        f'🏛 {quote(location.name)}',
        f'📍 {quote(location.address)}',
    ])

    return _make_message_by_rows(rows)


def _make_message_by_rows(
        rows: list[str],
) -> str:
    """Формирование сообщения из списка строк"""
    return '\n'.join(rows)
