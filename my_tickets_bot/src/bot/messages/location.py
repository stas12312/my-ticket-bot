from aiogram import types
from aiogram.utils.markdown import bold, italic, link

from bot.keyboards.location import get_locations_menu
from models import Location
from services.repositories import Repo
from .utils import quote, make_message_by_rows


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


def make_location_message(
        location: Location,
) -> str:
    """Формирования сообщения для локации"""

    url_name = link(location.name, location.url)

    rows = [
        f'🏛 _{url_name}_',
        f'📍 {quote(location.city.name)}, {quote(location.address)}',
    ]
    return make_message_by_rows(rows)


async def get_show_locations_params(
        user_id: int,
        city_id: int,
        repo: Repo,
) -> tuple[str, types.InlineKeyboardMarkup]:
    """Получение параметров для отображения списка мест"""
    city = await repo.city.get(user_id, city_id)
    locations = await repo.location.list(user_id, city_id)

    keyboard = get_locations_menu(city_id, locations)
    msg = f'🎭 _Ваши места в городе {quote(city.name)}_ \n\n' \
          f'ℹ️ Выберите место'
    return msg, keyboard
