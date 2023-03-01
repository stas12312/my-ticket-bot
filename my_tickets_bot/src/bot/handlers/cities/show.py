from aiogram import types, Router, F

from bot.callbacks import CityCallback, EntityAction
from bot.keyboards.city import get_actions_for_city
from bot.messages.city import make_city_message, get_show_cities_params
from services.repositories import Repo


async def show_cities(
        query: types.CallbackQuery,
        repo: Repo,
):
    """Отображение списка городов в inline-клавиатуре"""
    msg, keyboard = await get_show_cities_params(query.from_user.id, repo)
    await query.message.edit_text(msg, reply_markup=keyboard)


async def show_city(
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
router.callback_query.register(show_cities, CityCallback.filter(F.action == EntityAction.LIST))
router.callback_query.register(show_city, CityCallback.filter(F.action == EntityAction.SHOW))
