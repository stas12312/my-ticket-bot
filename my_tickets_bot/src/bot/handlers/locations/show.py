from aiogram import types, Router, F

from bot.callbacks import LocationCallback, EntityAction
from bot.keybaords import get_locations_menu, get_actions_for_location
from bot.messages import make_location_message, quote
from services.repositories import Repo


async def show_city_locations(
        query: types.CallbackQuery,
        callback_data: LocationCallback,
        repo: Repo,
):
    """Отображение мест пользователя"""
    city_id = callback_data.city_id
    city = await repo.city.get(query.from_user.id, city_id)
    locations = await repo.location.list(query.from_user.id, city_id)

    menu = get_locations_menu(city_id, locations)

    await query.message.edit_text(
        text=f'🎭 _Ваши места в городе {quote(city.name)}_ \n\n'
             f'ℹ️ Выберите место',
        reply_markup=menu,
    )


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
