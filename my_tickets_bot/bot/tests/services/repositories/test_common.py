"""Тесты общих запросов"""
import datetime

import pytest

from models import Location, User
from services.repositories import Repo


@pytest.mark.asyncio
async def test_get_statistic(
        repo: Repo,
        user: User,
        location: Location,
):
    """Тест получения статистики"""
    now = datetime.datetime(2023, 2, 1)

    # Мероприятия прошли
    await repo.event.save(user.user_id, 'Прошедшее 1', datetime.datetime(2022, 1, 2), location.location_id)
    await repo.event.save(user.user_id, 'Прошедшее 2', datetime.datetime(2022, 1, 3), location.location_id)
    await repo.event.save(user.user_id, 'Прошедшее 3', datetime.datetime(2023, 1, 4), location.location_id)

    # Планируются
    await repo.event.save(user.user_id, 'Планируется 1', datetime.datetime(2023, 2, 3), location.location_id)
    await repo.event.save(user.user_id, 'Планируется 2', datetime.datetime(2024, 1, 2), location.location_id)
    statistic = await repo.common.get_user_statistic(user.user_id, now)

    assert statistic[0].year == 2022
    assert statistic[0].is_past is True
    assert statistic[0].count == 2

    assert statistic[1].year == 2023
    assert statistic[1].is_past is True
    assert statistic[1].count == 1

    assert statistic[2].year == 2023
    assert statistic[2].is_past is False
    assert statistic[2].count == 1

    assert statistic[3].year == 2024
    assert statistic[3].is_past is False
    assert statistic[3].count == 1
