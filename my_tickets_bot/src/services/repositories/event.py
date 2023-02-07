import datetime

import asyncpg

from models import City, Location
from models.event import Event
from .queries import event as q


class EventRepo:
    """Репозиторий для события"""

    def __init__(
            self,
            connection: asyncpg.Connection,
    ):
        self._conn = connection

    async def save(
            self,
            user_id: int,
            name: str,
            event_time: datetime.datetime,
            location_id: int,
            link: str | None,
    ) -> Event:
        """Сохранения события"""

        record = await self._conn.fetchrow(q.SAVE_EVENT, user_id, name, event_time, link, location_id)
        return _convert_record_to_event(record)

    async def list(
            self,
            user_id: int,
    ) -> list[Event]:
        """Получение списка событий"""
        records = await self._conn.fetch(q.GET_EVENTS, user_id, None)

        return [_convert_record_to_event(record) for record in records]

    async def get(
            self,
            user_id: int,
            event_id: int,
    ) -> Event | None:
        """Получение события по идентификатору"""
        records = await self._conn.fetch(q.GET_EVENTS, user_id, event_id)

        return _convert_record_to_event(records[0]) if records else None

    async def delete(
            self,
            user_id: int,
            event_id: int,
    ):
        """Удаление события"""
        await self._conn.fetch(q.DELETE_EVENT, user_id, event_id)

def _convert_record_to_event(
        record: asyncpg.Record,
) -> Event:
    """Конвертация рекорда в событие"""
    return Event(
        event_id=record.get('event_id'),
        name=record.get('event_name'),
        time=record.get('event_time'),
        link=record.get('event_link'),
        location=Location(
            location_id=record.get('location_id'),
            name=record.get('location_name'),
            address=record.get('location_address'),
            city=City(
                city_id=record.get('city_id'),
                name=record.get('city_name'),
            ),
        )
    )
