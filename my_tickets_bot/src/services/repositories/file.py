import asyncpg

from models.file import File
from .queries import file as query


class FileRepo:

    def __init__(
            self,
            connection: asyncpg.Connection,
    ):
        self._conn = connection

    async def save_file(
            self,
            location: str,
            file_type: int,
    ) -> File:
        """Сохранение файла"""
        raw_file = await self._conn.fetchrow(query.SAVE_FILE, location, file_type)

        return File(
            file_id=raw_file['id'],
            location=raw_file['location'],
            file_type=raw_file['type'],
        )
