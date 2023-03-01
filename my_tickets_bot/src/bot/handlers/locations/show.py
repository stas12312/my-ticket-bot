from aiogram import types, Router, F

from bot.callbacks import LocationCallback, EntityAction
from bot.keyboards.location import get_actions_for_location
from bot.messages.location import make_location_message, get_show_locations_params
from services.repositories import Repo


async def show_city_locations(
        query: types.CallbackQuery,
        callback_data: LocationCallback,
        repo: Repo,
):
    """Отображение мест пользователя"""
    city_id = callback_data.city_id
    msg, keyboard = await get_show_locations_params(query.from_user.id, city_id, repo)

    await query.message.edit_text(msg, reply_markup=keyboard)


async def show_location(
        query: types.CallbackQuery,
        callback_data: LocationCallback,
        repo: Repo,
):
    """Отображение места проведения"""
    location_id = callback_data.location_id

    location = await repo.location.get(query.from_user.id, location_id)
    menu = get_actions_for_location(location.city.city_id, location.location_id)
    await query.message.edit_text(
        text=make_location_message(location),
        reply_markup=menu,
        disable_web_page_preview=True,
    )


router = Router()
router.callback_query.register(
    show_city_locations,
    LocationCallback.filter(
        (F.action == EntityAction.LIST)
        & (F.city_id.func(lambda v: v is not None))
    )
)
router.callback_query.register(show_location, LocationCallback.filter(F.action == EntityAction.SHOW))
