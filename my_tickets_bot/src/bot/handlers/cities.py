"""Обработчики для работы с городами"""
from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext

from services.city import get_timezone_name
from services.repository import Repo
from ..callbacks import CityCallback, EntityAction
from ..forms import CityForm
from ..keybaords import get_cities_menu, get_actions_for_city


async def show_cities_handler(
        query: types.CallbackQuery,
        repo: Repo,
):
    """Отображение списка городов в inline-клавиатуре"""

    cities = await repo.get_cities(query.from_user.id)
    menu = get_cities_menu(cities)
    await query.message.edit_text('Ваши города', reply_markup=menu)


async def show_city_handler(
        query: types.CallbackQuery,
        callback_data: CityCallback,
        repo: Repo,
):
    """Отображение города"""

    city_id = callback_data.city_id
    city = await repo.get_city(query.from_user.id, city_id)

    text = f'Город: {city.name}\n' \
           f'Временная зона: {city.timezone}'

    keyboard = get_actions_for_city(city_id)

    await query.message.edit_text(text, reply_markup=keyboard)


async def delete_city(
        query: types.CallbackQuery,
        callback_data: CityCallback,
        repo: Repo,
):
    """Удаление города"""

    city_id = callback_data.city_id
    await repo.delete_city(query.from_user.id, city_id)
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
    timezone_name = await get_timezone_name(name)
    if timezone_name is None:
        await message.answer(f'Не удалось найти город "{name}", попробуйте еще раз')
        return

    await state.clear()
    added_city = await repo.create_city(message.from_user.id, name, timezone_name)

    await message.answer(f'Город {added_city.name} с временной зоной {added_city.timezone} успешно добавлен')


cities_handler = Router()
cities_handler.callback_query.register(show_cities_handler, CityCallback.filter(F.action == EntityAction.list))
cities_handler.callback_query.register(start_add_city_handler, CityCallback.filter(F.action == EntityAction.add))
cities_handler.callback_query.register(show_city_handler, CityCallback.filter(F.action == EntityAction.show))
cities_handler.callback_query.register(delete_city, CityCallback.filter(F.action == EntityAction.delete))
cities_handler.message.register(processing_name_handler, CityForm.name)
