"""Репозиторий для общих запретов"""
import dataclasses
import datetime

import asyncpg

from .queries import common as q


@dataclasses.dataclass
class YearStatistic:
    """Статистика"""
    year: int
    count: int
    is_past: bool


class CommonRepo:
    """Репозиторий для общих запретов"""

    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def get_user_statistic(
            self,
            user_id: int,
            now: datetime.datetime,
    ) -> list[YearStatistic]:
        """Получение статистики пользователя"""
        records = await self._conn.fetch(q.GET_USER_STATISTIC, user_id, now)
        return [_convert_record_to_statistic(r) for r in records]


def _convert_record_to_statistic(record: asyncpg.Record) -> YearStatistic:
    """Преобразование рекорда в строку статистики"""
    return YearStatistic(
        year=record['year'],
        count=record['count'],
        is_past=record['is_past']
    )
