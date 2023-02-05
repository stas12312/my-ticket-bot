import asyncpg
from asyncpg import Connection

from models import Place, City
from .queries import place as query


class PlaceRepo:
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
    ) -> list[Place]:
        """Получение списка мест"""
        raw_places = await self._conn.fetch(query.GET_PLACES, user_id, city_id)

        places: list[Place] = []

        for place in raw_places:
            places.append(Place(
                place_id=place['id'],
                name=place['name'],
                address=place['address'],
                city=City(
                    city_id=place['city_id'],
                    name=place['city_name'],
                    timezone=None,
                ),
            ))
        return places

    async def save(
            self,
            city_id: int,
            name: str,
            address: str,
    ) -> Place:
        """Сохранение места"""
        raw_place = await self._conn.fetchrow(query.SAVE_PLACE, city_id, name, address)

        return Place(
            place_id=raw_place['id'],
            name=raw_place['name'],
            address=raw_place['address'],
            city=None,
        )

    async def delete(
            self,
            user_id: int,
            place_id: int,
    ):
        """Удаление места"""
        await self._conn.fetch(query.DELETE_PLACE, user_id, place_id)

    async def get(
            self,
            user_id: int,
            place_id: int,
    ):
        """Получение места для пользователя"""
        raw_place = await self._conn.fetchrow(query.GET_PLACE, user_id, place_id)

        return _convert_record_to_place(raw_place)

    async def get_by_name(
            self,
            user_id: int,
            place_name: str,
    ) -> Place | None:
        """Получение места по названию"""
        raw_place = await self._conn.fetchrow(query.GET_PLACE_BY_NAME, user_id, place_name)
        return _convert_record_to_place(raw_place)


def _convert_record_to_place(record: asyncpg.Record) -> Place:
    """Конвертация рекорда в модель"""
    return Place(
        place_id=record['id'],
        name=record['name'],
        address=record['address'],
        city=City(
            city_id=record['city_id'],
            name=record['city_name'],
            timezone=None,
        ),
    )
