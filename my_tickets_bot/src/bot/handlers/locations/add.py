import validators
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot.buttons import Action
from bot.callbacks import LocationCallback, EntityAction
from bot.forms import LocationForm
from bot.keybaords import get_menu_keyboard, get_keyboard_by_values
from bot.services.locations.messages import make_location_message
from services.repositories import Repo


async def start_add_location_handler(
        query: types.CallbackQuery,
        callback_data: LocationCallback,
        state: FSMContext,
):
    """Начало добавления места"""
    await query.message.edit_text('Введите название места')
    city_id = callback_data.city_id
    await state.set_state(LocationForm.input_name)
    await state.update_data(city_id=city_id)


async def processing_name_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введённого названия"""
    name = message.text
    await state.update_data(name=name)
    await message.answer('Введите адрес места')
    await state.set_state(LocationForm.input_address)


async def processing_address_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введенного адреса и сохранение места"""

    await state.update_data(address=message.text)
    keyboard = get_keyboard_by_values([Action.PASS])
    await message.answer('Введите ссылку на сайт', reply_markup=keyboard)
    await state.set_state(LocationForm.input_url)


async def processing_url(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка ссылки"""
    data = await state.get_data()
    address = data['address']
    city_id = data['city_id']
    name = data['name']
    url = None
    if message != Action.PASS:
        url = message.text
        if not validators.url(message.text):
            await message.answer('Некорректная ссылка, попробуйте еще раз')
            return

    db_location = await repo.location.save(city_id, name, address, url)
    location = await repo.location.get(message.from_user.id, db_location.location_id)

    await message.answer(
        f'✅ Место добавлено ✅\n\n{make_location_message(location)}',
        reply_markup=get_menu_keyboard(),
    )
    await state.clear()


router = Router()
router.callback_query.register(
    start_add_location_handler,
    LocationCallback.filter(
        (F.action == EntityAction.ADD)
        & (F.city_id.func(lambda v: v is not None)),
    )
)
router.message.register(processing_name_handler, LocationForm.input_name)
router.message.register(processing_address_handler, LocationForm.input_address)
router.message.register(processing_url, LocationForm.input_url)
