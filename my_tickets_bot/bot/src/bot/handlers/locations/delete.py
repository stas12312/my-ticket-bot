from aiogram import types, Router, F

from bot.callbacks import LocationCallback, EntityAction
from bot.messages.location import get_show_locations_params
from services.repositories import Repo


async def delete_location_handler(
        query: types.CallbackQuery,
        callback_data: LocationCallback,
        repo: Repo,
):
    """Удаление места"""
    location_id = callback_data.location_id
    city_id = callback_data.city_id
    await repo.location.delete(query.from_user.id, location_id)
    msg, keyboard = await get_show_locations_params(query.from_user.id, city_id, repo)

    await query.message.edit_text(msg, reply_markup=keyboard)
    await query.answer('Место удалено')


router = Router()

router.callback_query.register(
    delete_location_handler, LocationCallback.filter(F.action == EntityAction.DELETE),
)
