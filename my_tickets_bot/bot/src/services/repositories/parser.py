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

    async def all(self) -> list[Record]:
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

    async def get_supported_locations(
            self,
            user_id: int,
    ) -> list[Record]:
        """Получение локаций с поддержкой афиши"""
        result = await self._conn.fetch(query.GET_SUPPORTER_LOCATIONS, user_id)
        return result

    async def get_parser_events(
            self,
            parser_id: int,
            limit: int,
            offset: int,
    ) -> list[Record]:
        """Получение событий из парсера"""
        result = await self._conn.fetch(query.LIST_PARSER_EVENTS, parser_id, limit, offset)
        return result

    async def get_parser_events_count(
            self,
            parser_id: int,
    ) -> int:
        """Получение количества событий парсера"""
        return await self._conn.fetchval(query.COUNT_PARSER_EVENTS, parser_id)
