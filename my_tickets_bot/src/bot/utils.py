"""Вспомогательные функции"""
import logging
from collections.abc import Callable
from enum import IntEnum

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import File, Message

from models.file import File as TicketFile
from services.repositories import Repo

MAX_LENGTH = 4096


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
    message_parts = split_long_message(message)
    try:
        for message_part in message_parts:
            await bot.send_message(
                chat_id=user_id,
                text=message_part,
                **kwargs,
            )
    except exceptions.TelegramForbiddenError:
        logging.warning('User %s blocked bot', user_id)
    except exceptions.TelegramBadRequest:
        logging.error('Telegram bad request')


async def get_func_for_file(
        bot: Bot,
        file: TicketFile,
) -> Callable:
    """Получение функции для отправки файла"""
    file = await bot.get_file(file.bot_file_id)
    return bot.send_document if get_file_type(file) == FileType.DOCUMENT else bot.send_photo


def split_long_message(
        message: str,
        split_sing: str = '\n',
) -> list[str]:
    """Разбивка большого сообщения на части"""
    sing_len = len(split_sing)
    parts_by_sing = message.split(split_sing)
    result_parts: list[str] = []

    length = 0
    current_parts: list[str] = []
    for part in parts_by_sing:
        # Если часть превышаем лимит, разделим на части по максимальной длине
        if len(part) > MAX_LENGTH:
            result_parts.extend([part[i:i + MAX_LENGTH] for i in range(0, len(part), MAX_LENGTH)])
            continue

        if (len(part) + sing_len + length) > MAX_LENGTH:
            result_parts.append(split_sing.join(current_parts))
            length = 0
            current_parts = []

        current_parts.append(part)
        length += len(part) + sing_len

    if current_parts:
        result_parts.append(split_sing.join(current_parts))
    return result_parts
