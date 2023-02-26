"""Формирование красивых сообщений"""

from aiogram.utils.markdown import bold, italic
from aiogram.utils.text_decorations import markdown_decoration

from models import Location, City


def quote(
        value: str
) -> str:
    """Экранирование"""
    return markdown_decoration.quote(value)


TIME_EXAMPLES = f'Примеры:\n' \
                f'_{quote("20.03.23 20:00")}_\n' \
                f'_{quote("20.03 19:00")}_\n' \
                f'_{quote("20 марта 21:30")}_'


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
