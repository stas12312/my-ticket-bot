"""Формирование красивых сообщений"""
import datetime

from aiogram.utils.markdown import bold, link, italic
from aiogram.utils.text_decorations import markdown_decoration

from bot.emoji import get_clock_emoji
from models import Event, Location, City


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

    rows = [
        f'🎟 Билет на *{event_link}*',
        f'📍 {get_full_address_message(event.location)}',
        f'{get_clock_emoji(event.time)} {bold(beatify_date(event.time))}',
    ]

    if with_command:
        command = quote(f'/event_{event.event_id}')
        rows.append(f'⚙ Управлять билетами: {command}')

    return _make_message_by_rows(rows)


def get_full_address_message(
        location: Location,
) -> str:
    """Получение строки для адреса"""
    address = f'{quote(location.city.name)}, {quote(location.address)}'
    return f'{bold(location.name)} ' \
           f'{italic(address)}'


def beatify_date(raw_datetime: datetime.datetime) -> str:
    """Преобразование даты в корректное представление"""

    return raw_datetime.strftime('%d.%m.%Y %H:%M')


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
