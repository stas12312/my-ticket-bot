from asyncpg import Connection, Record

from .queries import parser as query


class ParserRepo:
    """Репозиторий для парсеров"""

    def __init__(
            self,
            connection: Connection,
    ):
        self._conn = connection

    async def list(self) -> list[Record]:
        """Список парсеров"""
        return await self._conn.fetch(query.LIST)
