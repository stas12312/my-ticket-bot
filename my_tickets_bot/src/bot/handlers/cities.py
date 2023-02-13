"""Обработчики для работы с городами"""
from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext

from services.city import get_timezone_name
from services.repositories import Repo
from ..callbacks import CityCallback, EntityAction
from ..forms import CityForm, LocationForm
from ..keybaords import get_cities_menu, get_actions_for_city
from ..messages import make_city_message, quote


async def show_cities_handler(
        query: types.CallbackQuery,
        repo: Repo,
):
    """Отображение списка городов в inline-клавиатуре"""

    cities = await repo.city.list(query.from_user.id)
    menu = get_cities_menu(cities)
    await query.message.edit_text('Ваши города', reply_markup=menu)


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


async def delete_city(
        query: types.CallbackQuery,
        callback_data: CityCallback,
        repo: Repo,
):
    """Удаление города"""

    city_id = callback_data.city_id
    await repo.city.delete(query.from_user.id, city_id)
    await query.message.edit_text('Город удалён')


async def start_add_city_handler(
        query: types.CallbackQuery,
        state: FSMContext,
):
    """Начало процесса добавления города"""
    await state.set_state(CityForm.name)
    await query.message.delete()
    await query.message.answer('Введите название города')


async def processing_name_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """
    Обработка введенного названия города,
    для дальнейшей корректной работы требуется наличие названия часового пояса
    который будет получен по названию города
    """
    name = message.text
    if (timezone_name := await get_timezone_name(name)) is None:
        await message.answer(f'Не удалось найти город "{quote(name)}", попробуйте еще раз')
        return

    await state.clear()

    city = await repo.city.get_by_name(message.from_user.id, name, True)
    if not city:
        added_city = await repo.city.create(message.from_user.id, name, timezone_name)
        await message.answer(f'✅ Город добавлен ✅ \n\n{make_city_message(added_city)}')
        # Запускаем диалог добавления места
        await message.answer('Введите название места проведения мероприятий')
        await state.set_state(LocationForm.name)
        await state.update_data(city_id=added_city.city_id)
    elif city.is_deleted:
        await repo.city.restore(message.from_user.id, city.city_id)
        await message.answer('✅ Город был восстановлен ✅')
    else:
        await message.answer('⚠️ Данный город уже добавлен ⚠️')

cities_handler = Router()
cities_handler.callback_query.register(show_cities_handler, CityCallback.filter(F.action == EntityAction.LIST))
cities_handler.callback_query.register(start_add_city_handler, CityCallback.filter(F.action == EntityAction.ADD))
cities_handler.callback_query.register(show_city_handler, CityCallback.filter(F.action == EntityAction.SHOW))
cities_handler.callback_query.register(delete_city, CityCallback.filter(F.action == EntityAction.DELETE))
cities_handler.message.register(processing_name_handler, CityForm.name)
