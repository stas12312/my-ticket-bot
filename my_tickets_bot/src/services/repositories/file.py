import asyncpg

from models.file import File
from .queries import file as query


class FileRepo:
    """Репозиторий файла"""

    def __init__(
            self,
            connection: asyncpg.Connection,
    ):
        self._conn = connection

    async def save_file(
            self,
            ticket_id: int,
            location: str,
            bot_file_id: str,
    ) -> File:
        """Сохранение файла"""
        record = await self._conn.fetchrow(query.SAVE_FILE, ticket_id, location, bot_file_id)
        return _convert_record_to_file(record)


def _convert_record_to_file(record: asyncpg.Record) -> File:
    """Конвертация рекорда в файл"""

    return File(
        file_id=record.get('file_id'),
        ticket_id=record.get('ticket_id'),
        location=record.get('file_location'),
        bot_file_id=record.get('bot_file_id'),
    )
