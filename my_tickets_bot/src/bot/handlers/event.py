"""Обработчики для работы с билетами"""
import validators
from aiogram import Router, F
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, CallbackQuery

from services.event_time import parse_datetime
from services.repositories import Repo
from ..buttons import MainMenu
from ..callbacks import EventCallback, EntityAction
from ..forms import EventForm
from ..keybaords import get_keyboard_by_values, get_menu_keyboard, get_actions_for_event
from ..messages import make_event_message


async def add_ticket_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Добавление события"""
    cities = await repo.city.list(message.from_user.id)

    keyboard = get_keyboard_by_values([city.name for city in cities])

    await message.answer('Выберите город', reply_markup=keyboard)
    await state.set_state(EventForm.city_id)


async def processing_city_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка места"""
    city_name = message.text

    if (city := await repo.city.get_by_name(message.from_user.id, city_name)) is None:
        await message.answer('Не удалось определить города, повторите попытку')
        return

    places = await repo.location.list(message.from_user.id, city.city_id)
    keyboard = get_keyboard_by_values([place.name for place in places])

    await message.answer('Выберите место проведения', reply_markup=keyboard)

    await state.update_data(city_id=city.city_id)
    await state.set_state(EventForm.location_id)


async def processing_place_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка выбранного место"""
    location_name = message.text

    if (location := await repo.location.get_by_name(message.from_user.id, location_name)) is None:
        await message.answer('Не удалось определить место, повторите попытку')
        return

    await message.answer('Введите название мероприятия', reply_markup=types.ReplyKeyboardRemove())

    await state.update_data(location_id=location.location_id)
    await state.set_state(EventForm.event_name)


async def processing_name_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введенного названия"""
    await message.answer('Отправьте ссылку на мероприятие')

    await state.update_data(event_name=message.text)
    await state.set_state(EventForm.event_link)


async def processing_link_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введения ссылки на мероприятие"""
    if not validators.url(message.text):
        await message.answer('Некорректная ссылка, попробуйте еще раз')
        return

    await state.update_data(event_link=message.text)
    await message.answer('Введите дату и время проведения мероприятия')
    await state.set_state(EventForm.event_time)


async def processing_event_time_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка введенной даты"""
    raw_datetime = message.text

    data = await state.get_data()
    city_id = data.get('city_id')
    city = await repo.city.get(message.from_user.id, city_id)

    if (parsed_datetime := parse_datetime(raw_datetime, city.timezone)) is None:
        await message.answer('Не удалось определить дату и время, попробуйте еще раз')
        return

    await message.answer('Отправьте билет')

    await state.update_data(event_time=parsed_datetime)
    await state.set_state(EventForm.file_id)


async def processing_file(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка файла"""
    data = await state.get_data()

    file_id = message.document.file_id if message.document else message.photo[-1].file_id

    event = await repo.event.save(
        user_id=message.from_user.id,
        location_id=data['location_id'],
        name=data['event_name'],
        event_time=data['event_time'],
        link=data['event_link'],
    )

    ticket = await repo.ticket.save(event.event_id)
    await repo.file.save_file(ticket.ticket_id, None, file_id)

    await message.answer('Билет успешно добавлен', reply_markup=get_menu_keyboard())
    await state.clear()


async def my_events_handler(
        message: types.Message,
        repo: Repo,
):
    """Отображения событий пользователя"""
    events = await repo.event.list(message.from_user.id)

    events_message = [make_event_message(ticket, with_command=True) for ticket in events]

    msg = '\n\n'.join(events_message) or 'У вас нет билетов'

    await message.answer(msg, disable_web_page_preview=True)


async def event_card_handler(
        message: types.Message,
        repo: Repo,
):
    """Получение карточки билета"""
    event_id = int(message.text.split('_')[1])
    event = await repo.event.get(message.from_user.id, event_id)
    tickets = await repo.ticket.list_for_event(message.from_user.id, event.event_id)

    event_message = make_event_message(event)
    keyboards = get_actions_for_event(event, tickets)

    await message.answer(
        text=event_message,
        reply_markup=keyboards,
        disable_web_page_preview=True,
    )


async def delete_event_handler(
        query: CallbackQuery,
        callback_data: EventCallback,
        repo: Repo,
):
    """Удаление события"""
    event_id = callback_data.event_id
    await repo.event.delete(query.from_user.id, event_id)
    await query.message.delete()
    await query.answer('Билеты удалены')


events_handler = Router()

events_handler.message.register(add_ticket_handler, Text(text=MainMenu.ADD_TICKET))
events_handler.message.register(my_events_handler, Text(text=MainMenu.MY_TICKETS))
events_handler.message.register(processing_city_handler, EventForm.city_id)
events_handler.message.register(processing_place_handler, EventForm.location_id)
events_handler.message.register(processing_name_handler, EventForm.event_name)
events_handler.message.register(processing_link_handler, EventForm.event_link)
events_handler.message.register(processing_event_time_handler, EventForm.event_time)
events_handler.message.register(processing_file, F.content_type.in_([ContentType.DOCUMENT, ContentType.PHOTO]))
events_handler.message.register(event_card_handler, Text(startswith='/event_'))
events_handler.callback_query.register(delete_event_handler, EventCallback.filter(F.action == EntityAction.delete))
