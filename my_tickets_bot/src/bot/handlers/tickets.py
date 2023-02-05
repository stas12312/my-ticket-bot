"""Обработчики для работы с билетами"""
import validators
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

from services.event_time import parse_datetime
from services.repositories import Repo
from ..buttons import MainMenu
from ..forms import TicketForm
from ..keybaords import get_keyboard_by_values, get_menu_keyboard
from ..messages import make_ticket_message


async def add_ticket_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Добавление билета"""
    cities = await repo.city.list(message.from_user.id)

    keyboard = get_keyboard_by_values([city.name for city in cities])

    await message.answer('Выберите город', reply_markup=keyboard)
    await state.set_state(TicketForm.city_id)


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

    places = await repo.place.list(message.from_user.id, city.city_id)
    keyboard = get_keyboard_by_values([place.name for place in places])

    await message.answer('Выберите место проведения', reply_markup=keyboard)

    await state.update_data(city_id=city.city_id)
    await state.set_state(TicketForm.place_id)


async def processing_place_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка выбранного место"""
    place_name = message.text

    if (place := await repo.place.get_by_name(message.from_user.id, place_name)) is None:
        await message.answer('Не удалось определить место, повторите попытку')
        return

    await message.answer('Введите название мероприятия', reply_markup=types.ReplyKeyboardRemove())

    await state.update_data(place_id=place.place_id)
    await state.set_state(TicketForm.event_name)


async def processing_name_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введенного названия"""
    await message.answer('Отправьте ссылку на мероприятие')

    await state.update_data(event_name=message.text)
    await state.set_state(TicketForm.event_link)


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
    await state.set_state(TicketForm.event_time)


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

    await message.answer('Отправьте файл билета')

    await state.update_data(event_time=parsed_datetime)
    await state.set_state(TicketForm.file_id)


async def processing_file(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
        bot: Bot,
):
    """Обработка файла"""
    data = await state.get_data()

    file_id = message.document.file_id if message.document else message.photo[-1].file_id
    bot_file = await bot.get_file(file_id)

    file = await repo.file.save_file(bot_file.file_path, 0)

    await repo.ticket.save(
        user_id=message.from_user.id,
        place_id=data['place_id'],
        event_name=data['event_name'],
        event_time=data['event_time'],
        event_link=data['event_link'],
        file_id=file.file_id,
    )
    await message.answer('Билет успешно добавлен', reply_markup=get_menu_keyboard())
    await state.clear()


async def my_tickets_handler(
        message: types.Message,
        repo: Repo,
):
    """Отображения билетов"""
    tickets = await repo.ticket.list(message.from_user.id)

    ticket_messages = [make_ticket_message(ticket, with_command=True) for ticket in tickets]

    tickets_messages = '\n\n'.join(ticket_messages)

    await message.answer(f'Ваши билеты\n\n{tickets_messages}', disable_web_page_preview=True)


tickets_handler = Router()

tickets_handler.message.register(add_ticket_handler, Text(text=MainMenu.ADD_TICKET))
tickets_handler.message.register(my_tickets_handler, Text(text=MainMenu.MY_TICKETS))
tickets_handler.message.register(processing_city_handler, TicketForm.city_id)
tickets_handler.message.register(processing_place_handler, TicketForm.place_id)
tickets_handler.message.register(processing_name_handler, TicketForm.event_name)
tickets_handler.message.register(processing_link_handler, TicketForm.event_link)
tickets_handler.message.register(processing_event_time_handler, TicketForm.event_time)
tickets_handler.message.register(processing_file, F.content_type.in_([ContentType.DOCUMENT, ContentType.PHOTO]))
