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
        records = await self._conn.fetch(q.GET_LOCATIONS, user_id, city_id)

        return [_convert_record_to_location(record) for record in records]

    async def save(
            self,
            city_id: int,
            name: str,
            address: str,
    ) -> Location:
        """Сохранение места"""
        record = await self._conn.fetchrow(q.SAVE_PLACE, city_id, name, address)

        return _convert_record_to_location(record)

    async def delete(
            self,
            user_id: int,
            place_id: int,
    ):
        """Удаление места"""
        await self._conn.fetch(q.DELETE_PLACE, user_id, place_id)

    async def get(
            self,
            user_id: int,
            place_id: int,
    ):
        """Получение места для пользователя"""
        raw_place = await self._conn.fetchrow(q.GET_PLACE, user_id, place_id)

        return _convert_record_to_location(raw_place)

    async def get_by_name(
            self,
            user_id: int,
            place_name: str,
    ) -> Location | None:
        """Получение места по названию"""
        raw_place = await self._conn.fetchrow(q.GET_PLACE_BY_NAME, user_id, place_name)
        return _convert_record_to_location(raw_place)


def _convert_record_to_location(record: asyncpg.Record) -> Location:
    """Конвертация рекорда в модель"""
    return Location(
        location_id=record.get('id'),
        name=record.get('name'),
        address=record.get('address'),
        city=City(
            city_id=record.get('city_id'),
            name=record.get('city_name'),
            timezone=None,
        ),
    )
