from aiogram import types, Router, F

from bot.callbacks import LocationCallback, EntityAction
from services.repositories import Repo


async def delete_location_handler(
        query: types.CallbackQuery,
        callback_data: LocationCallback,
        repo: Repo,
):
    """Удаление места"""
    location_id = callback_data.location_id
    await repo.location.delete(query.from_user.id, location_id)
    await query.answer('Место удалено')
    await query.message.delete()


router = Router()

router.callback_query.register(
    delete_location_handler, LocationCallback.filter(F.action == EntityAction.DELETE),
)
