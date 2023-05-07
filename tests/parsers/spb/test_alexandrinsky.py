import datetime
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from parsers.spb import AlexandrinskySpb
from services.poster import Event


# pylint: disable=unused-argument
async def get_data(url: str, params: dict, headers: dict | None = None) -> str:
    """Получение страницы"""

    if params['PAGEN_2'] == 0:
        path = Path(os.path.dirname(os.path.realpath(__file__)), 'files/alexandrinsky-1.html')
        with path.open(encoding='UTF-8') as file:
            return file.read()

    if params['PAGEN_2'] == 1:
        path = Path(os.path.dirname(os.path.realpath(__file__)), 'files/alexandrinsky-2.html')
        with path.open(encoding='UTF-8') as file:
            return file.read()


# pylint: disable=invalid-name
@pytest.mark.asyncio
async def test_big_dramatic_theatre_parser():
    """Проверка парсера"""

    parser = AlexandrinskySpb()
    parser.get_data_from_url = AsyncMock(side_effect=get_data)
    parser.get_now = MagicMock(return_value=datetime.datetime(2023, 1, 1))
    events = await parser.get_events()

    assert len(events) == 3

    assert events[0] == Event(
        name='ЭКСКУРСИЯ «БЛИСТАТЕЛЬНЫЙ АЛЕКСАНДРИНСКИЙ ТЕАТР»',
        datetime=datetime.datetime(2023, 5, 7, 12, 0),
        url='https://alexandrinsky.ru/afisha-i-bilety/ekskursiya-blistatelnyy-aleksandrinskiy-teatr/',
    )

    assert events[1] == Event(
        name='ЭКСКУРСИЯ «ТЕАТРАЛЬНЫЙ ПРОЛОГ»',
        datetime=datetime.datetime(2023, 5, 20, 17, 0),
        url='https://alexandrinsky.ru/afisha-i-bilety/ekskursiya-teatralnyy-prolog/',
    )

    assert events[2] == Event(
        name='ЭКСКУРСИЯ «ТЕАТРАЛЬНЫЙ ПРОЛОГ»',
        datetime=datetime.datetime(2023, 6, 22, 18, 0),
        url='https://alexandrinsky.ru/afisha-i-bilety/ekskursiya-teatralnyy-prolog/',
    )
