from aiogram import types

from bot.keyboards.city import get_cities_menu
from models import City
from services.repositories import Repo
from .utils import quote, make_message_by_rows


def make_city_message(
        city: City,
) -> str:
    """Формирование сообщения для описания города"""
    rows = [
        f'🏘 _{quote(city.name)}_\n',
        f'🕰 {quote(city.timezone)}',
    ]
    return make_message_by_rows(rows)


async def get_show_cities_params(
        user_id: int,
        repo: Repo,
) -> tuple[str, types.InlineKeyboardMarkup]:
    """Получение сообщения и клавиатуры для списка городов"""
    cities = await repo.city.list(user_id)
    keyboard = get_cities_menu(cities)
    msg = '🏙 _Ваши города_\n\n' \
          'ℹ️ Выберите город'
    return msg, keyboard
