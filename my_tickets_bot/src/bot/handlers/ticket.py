"""Обработчики для билетов"""
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

from bot.callbacks import TicketCallback, EntityAction
from bot.forms import TicketForm
from bot.keybaords import get_actions_for_event, get_actions_for_ticket
from bot.services.events.messages import make_event_message
from bot.utils import save_ticket, get_func_for_file
from models import Ticket
from services.repositories import Repo


async def download_ticket_handler(
        query: types.CallbackQuery,
        callback_data: TicketCallback,
        repo: Repo,
        bot: Bot,
):
    """Обработка скачивание билета"""

    event_id = callback_data.event_id

    tickets = await repo.ticket.list_for_event(query.from_user.id, event_id)
    await query.answer()

    if not tickets:
        # Редактируем текущее сообщение для актуализации
        event = await repo.event.get(query.from_user.id, event_id)
        tickets = await repo.ticket.list_for_event(query.from_user.id, event_id)
        msg = make_event_message(event)
        keyboard = get_actions_for_event(event, tickets)
        await query.message.edit_text(msg, reply_markup=keyboard, disable_web_page_preview=True)

    for ticket in tickets:
        await send_ticket(bot, query.from_user.id, ticket, query.message.message_id)


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
    await message.answer('✅ Билет добавлен ✅')


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


async def send_ticket(
        bot: Bot,
        user_id: int,
        ticket: Ticket,
        reply_to_id: int | None = None,
):
    """Отправка билета"""
    func = await get_func_for_file(bot, ticket.file)
    keyboard = get_actions_for_ticket(ticket)
    await func(
        user_id,
        ticket.file.bot_file_id,
        reply_markup=keyboard,
        reply_to_message_id=reply_to_id,
    )


tickets_handler = Router()
tickets_handler.callback_query.register(download_ticket_handler, TicketCallback.filter(F.action == EntityAction.SHOW))
tickets_handler.callback_query.register(start_add_ticket_handler, TicketCallback.filter(F.action == EntityAction.ADD))
tickets_handler.message.register(
    save_ticket_handler,
    TicketForm.file,
    F.content_type.in_([ContentType.DOCUMENT, ContentType.PHOTO]),
)
tickets_handler.callback_query.register(delete_ticket_handler, TicketCallback.filter(F.action == EntityAction.DELETE))
