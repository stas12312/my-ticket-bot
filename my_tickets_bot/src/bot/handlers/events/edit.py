"""Редактирование мероприятия"""
import logging

import validators
from aiogram import Router, types, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from bot.callbacks import EventCallback, EntityAction, EditEventCallback, EditEventField
from bot.forms import EditEventForm
from bot.keybaords import get_actions_for_edit_event, get_menu_keyboard, get_keyboard_by_values
from bot.messages import TIME_EXAMPLES
from bot.services.events.messages import make_event_message
from services.event_time import parse_datetime, get_localtime
from services.repositories import Repo


async def delete_event_handler(
        query: types.CallbackQuery,
        callback_data: EventCallback,
        repo: Repo,
):
    """Удаление события"""
    event_id = callback_data.event_id
    await repo.event.delete(query.from_user.id, event_id)
    await query.message.delete()
    await query.answer('Билеты удалены')


async def edit_name_handler(
        query: types.CallbackQuery,
        callback_data: EditEventCallback,
        state: FSMContext
):
    """Редактирования названия события"""
    event_id = callback_data.event_id
    await state.set_state(EditEventForm.name)
    await state.update_data(event_id=event_id, message_id=query.message.message_id)
    await query.message.answer(
        text='Введите новое название',
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def edit_link_handler(
        query: types.CallbackQuery,
        callback_data: EditEventCallback,
        state: FSMContext,
):
    """Редактирование ссылки события"""
    event_id = callback_data.event_id
    await state.set_state(EditEventForm.link)
    await state.update_data(event_id=event_id, message_id=query.message.message_id)
    await query.message.answer(
        text='Введите новую ссылку',
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def edit_time_handler(
        query: types.CallbackQuery,
        callback_data: EditEventCallback,
        state: FSMContext,
):
    """Редактирование времени мероприятия"""
    event_id = callback_data.event_id
    await state.set_state(EditEventForm.time)
    await state.update_data(event_id=event_id, message_id=query.message.message_id)
    await query.message.answer(
        text=f'Введите новые дату и время проведения мероприятия\n{TIME_EXAMPLES}',
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def edit_location_city_handler(
        query: types.CallbackQuery,
        callback_data: EditEventCallback,
        state: FSMContext,
        repo: Repo,
):
    """
    Редактирование места
    Выбор города
    """
    event_id = callback_data.event_id
    await state.set_state(EditEventForm.city_id)
    await state.update_data(event_id=event_id, message_id=query.message.message_id)

    cities = await repo.city.list(query.from_user.id)

    keyboard = get_keyboard_by_values([c.name for c in cities])

    await query.message.answer(
        text='Выберите город',
        reply_markup=keyboard,
    )


async def edit_location_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """
    Редактирование места
    Выбор места
    """
    city_name = message.text
    city = await repo.city.get_by_name(message.from_user.id, city_name)
    if not city:
        await message.answer('Город не найден, попробуйте еще раз')
        return

    locations = await repo.location.list(message.from_user.id, city.city_id)
    keyboard = get_keyboard_by_values([l.name for l in locations])
    await message.answer('Выберите место', reply_markup=keyboard)
    await state.set_state(EditEventForm.location_id)


async def edit_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
        bot: Bot,
):
    """Сохранение новых параметров"""
    data = await state.get_data()
    message_id = data.get('message_id')
    event_id = data.get('event_id')

    current_state = await state.get_state()

    # Получаем текущее событие
    event = await repo.event.get(message.from_user.id, event_id)
    match current_state:
        case EditEventForm.name:
            event.name = message.text
        case EditEventForm.link:
            if not validators.url(message.text):
                await message.answer('Некорректная ссылка')
                return
            event.link = message.text

        case EditEventForm.time:
            now = get_localtime(event.location.city.timezone)
            parsed_datetime = parse_datetime(message.text, event.location.city.timezone, now)
            if not parsed_datetime:
                await message.answer('Некорректное время')
                return
            event.time = parsed_datetime
        case EditEventForm.location_id:
            location = await repo.location.get_by_name(message.from_user.id, message.text)
            if not location:
                await message.answer('Место не найдено, попробуйте еще раз')
                return
            event.location = location

    await repo.event.save(
        event_id=event_id,
        user_id=event.user.user_id,
        name=event.name,
        event_time=event.time,
        location_id=event.location.location_id,
        link=event.link,
    )

    new_event = await repo.event.get(message.from_user.id, event_id)
    event_message = make_event_message(new_event)
    keyboard = get_actions_for_edit_event(event_id)
    try:
        await bot.edit_message_text(event_message, message.from_user.id, message_id, reply_markup=keyboard)
    except TelegramBadRequest as exp:
        logging.error(exp)

    await state.clear()
    await message.answer('Событие изменено', reply_markup=get_menu_keyboard())


router = Router()
router.callback_query.register(delete_event_handler, EventCallback.filter(F.action == EntityAction.DELETE))
router.callback_query.register(edit_name_handler, EditEventCallback.filter(F.field_name == EditEventField.NAME))
router.callback_query.register(edit_link_handler, EditEventCallback.filter(F.field_name == EditEventField.LINK))
router.callback_query.register(edit_time_handler, EditEventCallback.filter(F.field_name == EditEventField.TIME))
router.callback_query.register(
    edit_location_city_handler,
    EditEventCallback.filter(F.field_name == EditEventField.LOCATION),
)
router.message.register(edit_location_handler, EditEventForm.city_id)
router.message.register(edit_handler, EditEventForm.name)
router.message.register(edit_handler, EditEventForm.link)
router.message.register(edit_handler, EditEventForm.time)
router.message.register(edit_handler, EditEventForm.location_id)
