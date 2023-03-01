from aiogram import types, Router, F

from bot.callbacks import CityCallback, EntityAction
from bot.services.cities.messages import get_show_cities_params
from services.repositories import Repo


async def delete_city(
        query: types.CallbackQuery,
        callback_data: CityCallback,
        repo: Repo,
):
    """Удаление города"""

    city_id = callback_data.city_id
    await repo.city.delete(query.from_user.id, city_id)
    msg, keyboard = await get_show_cities_params(query.from_user.id, repo)
    # Переходим в список городов
    await query.message.edit_text(msg, reply_markup=keyboard)
    await query.answer('Город удален')


router = Router()
router.callback_query.register(delete_city, CityCallback.filter(F.action == EntityAction.DELETE))
