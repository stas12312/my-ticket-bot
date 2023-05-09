import json

import asyncpg
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

    async def get(
            self,
            parser_id: int,
    ) -> dict | None:
        """Получение информации о парсере"""
        record: asyncpg.Record = await self._conn.fetchrow(query.GET, parser_id)
        if not record:
            return {}
        data = {**record}
        if data['events'] is not None:
            data['events'] = json.loads(data['events'])
        return data
