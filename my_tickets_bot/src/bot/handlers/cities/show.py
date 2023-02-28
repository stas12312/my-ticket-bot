from aiogram import types, Router, F

from bot.callbacks import CityCallback, EntityAction
from bot.keybaords import get_cities_menu, get_actions_for_city
from bot.messages import make_city_message
from services.repositories import Repo


async def show_cities_handler(
        query: types.CallbackQuery,
        repo: Repo,
):
    """Отображение списка городов в inline-клавиатуре"""

    cities = await repo.city.list(query.from_user.id)
    menu = get_cities_menu(cities)
    await query.message.edit_text(
        '🏙 _Ваши города_\n\n'
        'ℹ️ Выберите город',
        reply_markup=menu)


async def show_city_handler(
        query: types.CallbackQuery,
        callback_data: CityCallback,
        repo: Repo,
):
    """Отображение города"""

    city_id = callback_data.city_id
    city = await repo.city.get(query.from_user.id, city_id)

    text = make_city_message(city)

    keyboard = get_actions_for_city(city_id)

    await query.message.edit_text(text, reply_markup=keyboard)


router = Router()
router.callback_query.register(show_cities_handler, CityCallback.filter(F.action == EntityAction.LIST))
router.callback_query.register(show_city_handler, CityCallback.filter(F.action == EntityAction.SHOW))
