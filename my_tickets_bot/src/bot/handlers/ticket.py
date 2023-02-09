"""Обработчики для билетов"""
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

from bot.callbacks import TicketCallback, EntityAction
from bot.forms import TicketForm
from bot.keybaords import get_actions_for_event, get_actions_for_ticket
from bot.messages import make_event_message
from bot.utils import get_file_type, FileType, save_ticket
from services.repositories import Repo


async def download_ticket_handler(
        query: types.CallbackQuery,
        callback_data: TicketCallback,
        repo: Repo,
        bot: Bot,
):
    """Обработка скачивание билета"""

    ticket_id = callback_data.ticket_id
    event_id = callback_data.event_id
    ticket = await repo.ticket.get(query.from_user.id, ticket_id)

    if ticket is None:
        # Редактируем текущее сообщение для актуализации
        event = await repo.event.get(query.from_user.id, event_id)
        tickets = await repo.ticket.list_for_event(query.from_user.id, event_id)
        msg = make_event_message(event)
        keyboard = get_actions_for_event(event, tickets)
        await query.message.edit_text(msg, reply_markup=keyboard, disable_web_page_preview=True)

    file = await bot.get_file(ticket.file.bot_file_id)
    await query.answer()
    keyboard = get_actions_for_ticket(ticket)
    if get_file_type(file) == FileType.PHOTO:
        await query.message.answer_photo(ticket.file.bot_file_id, reply_markup=keyboard)
    else:
        await query.message.answer_document(ticket.file.bot_file_id, reply_markup=keyboard)


async def start_add_ticket_handler(
        query: types.CallbackQuery,
        callback_data: TicketCallback,
        state: FSMContext,
):
    """Начало добавление билета"""
    event_id = callback_data.event_id

    await state.set_state(TicketForm.file)
    await state.update_data(event_id=event_id)
    await query.message.answer('Отправьте файл билета')


async def save_ticket_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Сохранение билета"""
    data = await state.get_data()
    event_id = data['event_id']

    await save_ticket(
        event_id=event_id,
        message=message,
        repo=repo,
    )

    await state.clear()

    event = await repo.event.get(message.from_user.id, event_id)
    tickets = await repo.ticket.list_for_event(message.from_user.id, event_id)
    keyboard = get_actions_for_event(event, tickets)

    msg = make_event_message(event)
    await message.answer(
        text=msg,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


async def delete_ticket_handler(
        query: types.CallbackQuery,
        callback_data: TicketCallback,
        repo: Repo,

):
    """Удаление билета"""
    ticket_id = callback_data.ticket_id

    await repo.ticket.delete(query.from_user.id, ticket_id)
    await query.message.delete()
    await query.answer('Билет удален')


tickets_handler = Router()
tickets_handler.callback_query.register(download_ticket_handler, TicketCallback.filter(F.action == EntityAction.show))
tickets_handler.callback_query.register(start_add_ticket_handler, TicketCallback.filter(F.action == EntityAction.add))
tickets_handler.message.register(
    save_ticket_handler,
    TicketForm.file,
    F.content_type.in_([ContentType.DOCUMENT, ContentType.PHOTO]),
)
tickets_handler.callback_query.register(delete_ticket_handler, TicketCallback.filter(F.action == EntityAction.delete))
