"""Класс для работы с БД"""
import logging
from typing import Optional, List

from asyncpg import Connection, Record

from models import City
from . import sql

logger = logging.getLogger(__name__)


class Repo:

    def __init__(
            self,
            connection: Connection,
    ):
        self._conn = connection

    async def save_user(
            self,
            user_id: int,
            username: Optional[str],
    ) -> Record:
        """Сохранение пользователя"""
        logger.info('Сохранение пользователя')
        return await self._conn.fetchrow(sql.SAVE_USER, user_id, username)

    async def get_cities(
            self,
            user_id: int,
    ) -> List[City]:
        """Получение городов пользователя"""
        logger.info(f'Получение городов для {user_id}')
        raw_cities = await self._conn.fetch(sql.GET_USER_CITIES, user_id)

        cities: List[City] = []
        for city in raw_cities:
            cities.append(City(
                city_id=city['id'],
                name=city['name'],
                timezone=city['timezone']
            ))

        return cities

    async def create_city(
            self,
            user_id: int,
            name: str,
            timezone: str,
    ) -> City:
        """Сохранение города"""
        logger.info(f'Сохранение города {name} для {user_id}')

        raw_city = await self._conn.fetchrow(sql.CREATE_CITY, user_id, name, timezone)

        return City(
            city_id=raw_city['id'],
            name=raw_city['name'],
            timezone=raw_city['timezone'],
        )

    async def get_city(
            self,
            user_id: int,
            city_id: int,
    ) -> City:
        logger.info(f'Получение города {city_id} для {user_id}')

        raw_city = await self._conn.fetchrow(sql.GET_CITY, user_id, city_id)
        return City(
            city_id=raw_city['id'],
            name=raw_city['name'],
            timezone=raw_city['timezone'],
        )

    async def delete_city(
            self,
            user_id: int,
            city_id: int,
    ):
        logger.info(f'Удаление города {city_id} для {user_id}')

        await self._conn.fetch(sql.DELETE_CITY, user_id, city_id)