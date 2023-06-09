"""Статистика пользователя"""
import dataclasses
import datetime
from collections import defaultdict

from services.repositories import Repo


@dataclasses.dataclass
class RowStatistic:
    """Строка статистики"""
    year: int
    past_count: int
    planned_count: int


async def get_user_statistic(
        user_id: int,
        now: datetime.datetime,
        repo: Repo,
) -> list[RowStatistic]:
    """Получение статистики пользователя"""
    years_statistics = await repo.common.get_user_statistic(user_id, now)

    row_by_year = defaultdict(lambda: RowStatistic(0, 0, 0))

    for row in years_statistics:
        row_statistic = row_by_year[row.year]
        row_statistic.year = row.year
        if row.is_past:
            row_statistic.past_count = row.count
        else:
            row_statistic.planned_count = row.count

    return list(row_by_year.values())
