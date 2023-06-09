"""Репозиторий для таблицы городов"""
import asyncpg
from asyncpg import Connection

from models import City
from .queries import city as query


class CityRepo:
    """Репозиторий для города"""

    def __init__(
            self,
            connection: Connection,
    ):
        self._conn = connection

    async def list(
            self,
            user_id: int,
    ) -> list[City]:
        """Получение городов пользователя"""
        records = await self._conn.fetch(query.GET_USER_CITIES, user_id)
        return [_convert_record_to_city(record) for record in records]

    async def create(
            self,
            user_id: int,
            name: str,
            timezone: str,
    ) -> City:
        """Сохранение города"""

        record = await self._conn.fetchrow(query.CREATE_CITY, user_id, name, timezone)
        return _convert_record_to_city(record)

    async def user_has_cities(
            self,
            user_id: int,
            with_deleted: bool = False,
    ) -> bool:
        """Проверка наличия городов у пользователя"""
        return await self._conn.fetchval(query.USER_HAS_CITY, user_id, with_deleted)

    async def get(
            self,
            user_id: int,
            city_id: int,
    ) -> City:
        """Получение города для пользователя"""
        record = await self._conn.fetchrow(query.GET_CITY, user_id, city_id)
        return _convert_record_to_city(record)

    async def get_by_name(
            self,
            user_id: int,
            name: str,
            with_deleted: bool = False,
    ) -> City | None:
        """Получение города по названию"""
        record = await self._conn.fetchrow(query.GET_CITY_BY_NAME, user_id, name, with_deleted)
        return _convert_record_to_city(record) if record else None

    async def delete(
            self,
            user_id: int,
            city_id: int,
    ):
        """Удаление города"""
        await self._conn.fetch(query.DELETE_CITY, user_id, city_id)

    async def restore(
            self,
            user_id: int,
            city_id: int,
    ):
        """Восстановление города"""
        await self._conn.fetch(query.RESTORE, user_id, city_id)


def _convert_record_to_city(record: asyncpg.Record) -> City:
    """Конвертация рекорда в город"""
    return City(
        city_id=record.get('id'),
        name=record.get('name'),
        timezone=record.get('timezone'),
        is_deleted=record.get('is_deleted')
    )
