"""Вспомогательные функции"""
import logging
from collections.abc import Callable
from enum import IntEnum

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import File, Message

from models.file import File as TicketFile
from services.repositories import Repo


class FileType(IntEnum):
    """Типы файлов"""
    PHOTO = 0
    DOCUMENT = 1


def get_file_type(
        file: File,
) -> FileType:
    """Определение типа файла"""
    if file.file_path.startswith('documents'):
        return FileType.DOCUMENT
    return FileType.PHOTO


async def save_ticket(
        event_id: int,
        message: Message,
        repo: Repo,
):
    """Сохранение билета"""
    file_id = message.document.file_id if message.document else message.photo[-1].file_id

    ticket = await repo.ticket.save(event_id)
    await repo.file.save_file(ticket.ticket_id, None, file_id)


async def send_message_for_users(
        bot: Bot,
        user_ids: list[int],
        message: str,
):
    """Отправка сообщения пользователям"""
    for user_id in user_ids:
        await safe_send_message(bot, user_id, message)


async def safe_send_message(
        bot,
        user_id: int,
        message: str,
        **kwargs,
):
    """Безопасная отправка сообщения"""
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message,
            **kwargs,
        )
    except exceptions.TelegramForbiddenError:
        logging.warning('User %s blocked bot', user_id)


async def get_func_for_file(
        bot: Bot,
        file: TicketFile,
) -> Callable:
    """Получение функции для отправки файла"""
    file = await bot.get_file(file.bot_file_id)
    return bot.send_document if get_file_type(file) == FileType.DOCUMENT else bot.send_photo
