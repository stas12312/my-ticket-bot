"""Вспомогательные функции"""
from enum import IntEnum

from aiogram.types import File, Message

from services.repositories import Repo


class FileType(IntEnum):
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
