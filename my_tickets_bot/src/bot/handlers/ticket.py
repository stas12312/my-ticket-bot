from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from bot.callbacks import TicketCallback, EntityAction
from bot.utils import get_file_type, FileType
from services.repositories import Repo


async def download_ticket_handler(
        query: CallbackQuery,
        callback_data: TicketCallback,
        repo: Repo,
        bot: Bot,
):
    """Обработка скачивание билета"""
    ticket_id = callback_data.ticket_id
    ticket = await repo.ticket.get(query.from_user.id, ticket_id)

    file = await bot.get_file(ticket.file.bot_file_id)
    await query.answer()
    if get_file_type(file) == FileType.PHOTO:
        await query.message.answer_photo(ticket.file.bot_file_id)
    else:
        await query.message.answer_document(ticket.file.bot_file_id)


tickets_handler = Router()
tickets_handler.callback_query.register(download_ticket_handler, TicketCallback.filter(F.action == EntityAction.show))
