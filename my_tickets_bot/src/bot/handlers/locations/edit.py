import validators
from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext

from bot.callbacks.location import LocationEditCallback, LocationEditField
from bot.forms.location import LocationEditForm
from bot.keyboards.location import get_actions_for_edit
from bot.messages.location import make_location_message
from services.repositories import Repo


async def edit_name(
        query: types.CallbackQuery,
        callback_data: LocationEditCallback,
        state: FSMContext,
):
    """Редактирование названия"""
    await query.message.answer('Введите новое название')
    await state.set_state(LocationEditForm.name)
    await state.update_data(
        message_id=query.message.message_id,
        location_id=callback_data.location_id,
    )


async def edit_url(
        query: types.CallbackQuery,
        callback_data: LocationEditCallback,
        state: FSMContext,
):
    """Редактирование ссылки"""
    await query.message.answer('Введите новую ссылку')
    await state.set_state(LocationEditForm.url)
    await state.update_data(
        message_id=query.message.message_id,
        location_id=callback_data.location_id,
    )


async def edit_address(
        query: types.CallbackQuery,
        callback_data: LocationEditCallback,
        state: FSMContext,
):
    """Редактирование адреса"""
    await query.message.answer('Введите новый адрес')
    await state.set_state(LocationEditForm.address)
    await state.update_data(
        message_id=query.message.message_id,
        location_id=callback_data.location_id,
    )


async def save_changes(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
        bot: Bot,
):
    """Сохранение изменений"""
    data = await state.get_data()

    location_id = data.get('location_id')
    edit_message_id = data.get('message_id')
    location = await repo.location.get(message.from_user.id, location_id)
    input_text = message.text
    current_state = await state.get_state()
    match current_state:
        case LocationEditForm.name:
            location.name = input_text
        case LocationEditForm.url:
            if not validators.url(input_text):
                await message.answer('Некорректная ссылка, попробуйте еще раз')
                return
            location.url = input_text
        case LocationEditForm.address:
            location.address = input_text

    await repo.location.save(
        location_id=location.location_id,
        city_id=location.city.city_id,
        name=location.name,
        address=location.address,
        url=location.url,
    )
    msg = make_location_message(location)
    keyboard = get_actions_for_edit(location.city.city_id, location_id)
    await message.answer('Место изменено')
    await bot.edit_message_text(msg, message.from_user.id, edit_message_id, reply_markup=keyboard)
    await state.clear()


router = Router()
router.callback_query.register(edit_name, LocationEditCallback.filter(F.field == LocationEditField.NAME))
router.callback_query.register(edit_url, LocationEditCallback.filter(F.field == LocationEditField.URL))
router.callback_query.register(edit_address, LocationEditCallback.filter(F.field == LocationEditField.ADDRESS))
router.message.register(save_changes, LocationEditForm.name)
router.message.register(save_changes, LocationEditForm.url)
router.message.register(save_changes, LocationEditForm.address)
