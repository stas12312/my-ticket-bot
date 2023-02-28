from aiogram import types, Router, F

from bot.callbacks import CityCallback, EntityAction
from services.repositories import Repo


async def delete_city(
        query: types.CallbackQuery,
        callback_data: CityCallback,
        repo: Repo,
):
    """Удаление города"""

    city_id = callback_data.city_id
    await repo.city.delete(query.from_user.id, city_id)
    await query.message.edit_text('Город удалён')


router = Router()
router.callback_query.register(delete_city, CityCallback.filter(F.action == EntityAction.DELETE))
