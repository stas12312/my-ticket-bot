"""Проверка построения статистики"""
import datetime
from unittest.mock import AsyncMock

import pytest

from services.repositories import Repo
from services.repositories.common import YearStatistic
from services.statistic import get_user_statistic


@pytest.mark.asyncio
async def test_statistic(
        repo: Repo
):
    """Проверка построения статистики"""
    repo.common.get_user_statistic = AsyncMock(return_value=[
        YearStatistic(2022, 2, True),
        YearStatistic(2023, 5, True),
        YearStatistic(2023, 6, False),
    ])

    rows = await get_user_statistic(1, datetime.datetime.now(), repo)

    assert rows[0].year == 2022
    assert rows[0].past_count == 2
    assert rows[0].planned_count == 0

    assert rows[1].year == 2023
    assert rows[1].past_count == 5
    assert rows[1].planned_count == 6
