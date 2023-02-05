"""Обработчики для работ с местами мероприятий"""

from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext

from services.repositories import Repo
from ..callbacks import PlaceCallback, EntityAction
from ..forms import PlaceForm
from ..keybaords import get_places_menu, get_keyboard_by_values, get_menu_keyboard, get_actions_for_place


async def show_places_handler(
        query: types.CallbackQuery,
        repo: Repo,
):
    """Отображение мест пользователя"""

    places = await repo.place.list(query.from_user.id)

    menu = get_places_menu(places)

    await query.message.edit_text(
        text='Ваши места',
        reply_markup=menu,
    )


async def show_place_handler(
        query: types.CallbackQuery,
        callback_data: PlaceCallback,
        repo: Repo,
):
    """Отображение места проведения"""

    place_id = callback_data.place_id

    place = await repo.place.get(query.from_user.id, place_id)
    menu = get_actions_for_place(place_id)
    await query.message.edit_text(
        text='Место\n'
             f'Город: {place.city.name}\n'
             f'Название: {place.name}\n'
             f'Адрес: {place.address}',
        reply_markup=menu,
    )


async def delete_place_handler(
        query: types.CallbackQuery,
        callback_data: PlaceCallback,
        repo: Repo,
):
    """Удаление места"""
    place_id = callback_data.place_id
    await repo.place.delete(query.from_user.id, place_id)
    await query.answer('Место удалено', show_alert=True)
    await query.message.delete()


async def start_add_place_handler(
        query: types.CallbackQuery,
        state: FSMContext,
        repo: Repo,
):
    """Начало добавления места"""
    await query.message.delete()
    await state.set_state(PlaceForm.city_id)
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
    await state.set_state(PlaceForm.name)
    await message.answer('Введите название места', reply_markup=types.ReplyKeyboardRemove())


async def processing_name_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введённого названия"""
    name = message.text
    await state.update_data(name=name)
    await state.set_state(PlaceForm.address)
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

    place = await repo.place.save(city_id, name, address)

    await message.answer(f'Место {place.name} успешно добавлено', reply_markup=get_menu_keyboard())

    await state.clear()


places_handler = Router()
places_handler.callback_query.register(show_places_handler, PlaceCallback.filter(F.action == EntityAction.list))
places_handler.callback_query.register(start_add_place_handler, PlaceCallback.filter(F.action == EntityAction.add))
places_handler.message.register(processing_city_handler, PlaceForm.city_id)
places_handler.message.register(processing_name_handler, PlaceForm.name)
places_handler.message.register(processing_address_handler, PlaceForm.address)
places_handler.callback_query.register(show_place_handler, PlaceCallback.filter(F.action == EntityAction.show))
places_handler.callback_query.register(delete_place_handler, PlaceCallback.filter(F.action == EntityAction.delete))
