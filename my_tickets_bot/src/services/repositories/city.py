"""Репозиторий для таблицы городов"""
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
        raw_cities = await self._conn.fetch(query.GET_USER_CITIES, user_id)

        cities: list[City] = []
        for city in raw_cities:
            cities.append(City(
                city_id=city['id'],
                name=city['name'],
                timezone=city['timezone']
            ))

        return cities

    async def create(
            self,
            user_id: int,
            name: str,
            timezone: str,
    ) -> City:
        """Сохранение города"""

        raw_city = await self._conn.fetchrow(query.CREATE_CITY, user_id, name, timezone)

        return City(
            city_id=raw_city['id'],
            name=raw_city['name'],
            timezone=raw_city['timezone'],
        )

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
        raw_city = await self._conn.fetchrow(query.GET_CITY, user_id, city_id)
        return City(
            city_id=raw_city['id'],
            name=raw_city['name'],
            timezone=raw_city['timezone'],
        )

    async def get_by_name(
            self,
            user_id: int,
            name: str,
    ) -> City:
        """Получение города по названию"""

        raw_city = await self._conn.fetchrow(query.GET_CITY_BY_NAME, user_id, name)
        return City(
            city_id=raw_city['id'],
            name=raw_city['name'],
            timezone=raw_city['timezone'],
        )

    async def delete(
            self,
            user_id: int,
            city_id: int,
    ):
        """Удаление города"""
        await self._conn.fetch(query.DELETE_CITY, user_id, city_id)
