import asyncpg
from asyncpg import Connection

from models import City
from models.location import Location
from .queries import location as q


class LocationRepo:
    """Репозиторий для места"""

    def __init__(
            self,
            connection: Connection,
    ):
        self._conn = connection

    async def list(
            self,
            user_id: int,
            city_id: int | None = None,
    ) -> list[Location]:
        """Получение списка мест"""
        records = await self._conn.fetch(q.LIST, user_id, city_id)

        return [_convert_record_to_location(record) for record in records]

    async def save(
            self,
            city_id: int,
            name: str,
            address: str,
            url: str | None = None,
            location_id: int | None = None,
    ) -> Location:
        """Сохранение места"""
        if location_id is None:
            record = await self._conn.fetchrow(q.SAVE, city_id, name, address, url)
        else:
            record = await self._conn.fetchrow(q.UPDATE, location_id, city_id, name, address, url)
        return _convert_record_to_location(record)

    async def delete(
            self,
            user_id: int,
            location_id: int,
    ):
        """Удаление места"""
        await self._conn.fetch(q.DELETE, user_id, location_id)

    async def get(
            self,
            user_id: int,
            location_id: int,
    ):
        """Получение места для пользователя"""
        record = await self._conn.fetchrow(q.GET_LOCATION, user_id, location_id)

        return _convert_record_to_location(record)

    async def get_by_name(
            self,
            user_id: int,
            name: str,
    ) -> Location | None:
        """Получение места по названию"""
        raw_place = await self._conn.fetchrow(q.GET_BY_NAME, user_id, name)
        return _convert_record_to_location(raw_place)


def _convert_record_to_location(record: asyncpg.Record) -> Location:
    """Конвертация рекорда в модель"""
    return Location(
        location_id=record.get('id'),
        name=record.get('name'),
        address=record.get('address'),
        url=record.get('url'),
        city=City(
            city_id=record.get('city_id'),
            name=record.get('city_name'),
            timezone=None,
        ),
    )
