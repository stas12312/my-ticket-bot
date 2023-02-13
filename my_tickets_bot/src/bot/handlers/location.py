"""Обработчики для работ с местами мероприятий"""

from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext

from services.repositories import Repo
from ..callbacks import LocationCallback, EntityAction
from ..forms import LocationForm
from ..keybaords import get_locations_menu, get_keyboard_by_values, get_menu_keyboard, get_actions_for_location
from ..messages import make_location_message


async def show_locations_handler(
        query: types.CallbackQuery,
        repo: Repo,
):
    """Отображение мест пользователя"""

    locations = await repo.location.list(query.from_user.id)

    menu = get_locations_menu(locations)

    await query.message.edit_text(
        text='Ваши места',
        reply_markup=menu,
    )


async def show_location_handler(
        query: types.CallbackQuery,
        callback_data: LocationCallback,
        repo: Repo,
):
    """Отображение места проведения"""

    location_id = callback_data.location_id

    location = await repo.location.get(query.from_user.id, location_id)
    menu = get_actions_for_location(location.location_id)
    await query.message.edit_text(
        text=make_location_message(location),
        reply_markup=menu,
    )


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


async def start_add_location_handler(
        query: types.CallbackQuery,
        state: FSMContext,
        repo: Repo,
):
    """Начало добавления места"""
    await query.message.delete()
    await state.set_state(LocationForm.city_id)
    cities = await repo.city.list(query.from_user.id)

    keyboard = get_keyboard_by_values([city.name for city in cities])
    await query.message.answer('Выберите город', reply_markup=keyboard)


async def processing_city_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка введенного города"""
    city_name = message.text

    if (city := await repo.city.get_by_name(message.from_user.id, city_name)) is None:
        await message.answer('Не удалось определить города, выберите город из предложенных')
        return

    await state.update_data(city_id=city.city_id)
    await state.set_state(LocationForm.name)
    await message.answer('Введите название места', reply_markup=types.ReplyKeyboardRemove())


async def processing_name_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введённого названия"""
    name = message.text
    await state.update_data(name=name)
    await state.set_state(LocationForm.address)
    await message.answer('Введите адрес места')


async def processing_address_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка введенного адреса и сохранение места"""
    data = await state.get_data()
    address = message.text
    city_id = data['city_id']
    name = data['name']

    location = await repo.location.save(city_id, name, address)

    await message.answer(
        f'✅ Место добавлено ✅\n\n{make_location_message(location)}',
        reply_markup=get_menu_keyboard(),
    )

    await state.clear()


locations_handler = Router()
locations_handler.callback_query.register(
    show_locations_handler, LocationCallback.filter(F.action == EntityAction.LIST),
)
locations_handler.callback_query.register(
    start_add_location_handler, LocationCallback.filter(F.action == EntityAction.ADD),
)
locations_handler.message.register(processing_city_handler, LocationForm.city_id)
locations_handler.message.register(processing_name_handler, LocationForm.name)
locations_handler.message.register(processing_address_handler, LocationForm.address)
locations_handler.callback_query.register(
    show_location_handler, LocationCallback.filter(F.action == EntityAction.SHOW),
)
locations_handler.callback_query.register(
    delete_location_handler, LocationCallback.filter(F.action == EntityAction.DELETE),
)
