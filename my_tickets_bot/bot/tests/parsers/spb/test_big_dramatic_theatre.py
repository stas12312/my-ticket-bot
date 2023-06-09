import datetime
import os
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from parsers.spb import BigDramaticTheaterSpb
from services.poster import Event


# pylint: disable=unused-argument
async def get_data(url: str, params: dict, headers: dict | None = None) -> str:
    """Получение страницы"""

    if 'month' not in url:
        path = Path(os.path.dirname(os.path.realpath(__file__)), 'files/big-dramatic-theathre-1.html')
        with path.open(encoding='UTF-8') as file:
            return file.read()

    if 'month=6' in url:
        path = Path(os.path.dirname(os.path.realpath(__file__)), 'files/big-dramatic-theathre-2.html')
        with path.open(encoding='UTF-8') as file:
            return file.read()


# pylint: disable=invalid-name
@pytest.mark.asyncio
async def test_big_dramatic_theatre_parser():
    """Проверка парсера"""

    parser = BigDramaticTheaterSpb()
    parser.get_data_from_url = AsyncMock(side_effect=get_data)

    events = await parser.get_events()

    assert len(events) == 4

    assert events[0] == Event(
        name='Слава',
        url='https://bdt.spb.ru/spektakli/slava/',
        datetime=datetime.datetime(2023, 5, 1, 19, 00)
    )

    assert events[1] == Event(
        name='ПУТЕШЕСТВИЕ ЗА КУЛИСЫ БДТ',
        url='https://bdt.spb.ru/spektakli/puteshestvie-za-kulisy-bdt/',
        datetime=datetime.datetime(2023, 5, 1, 12, 00)
    )

    assert events[2] == Event(
        name='Дама с собачкой',
        url='https://bdt.spb.ru/spektakli/dama-s-sobachkoy/',
        datetime=datetime.datetime(2023, 5, 2, 19, 00)
    )

    assert events[3] == Event(
        name='Привидения',
        url='https://bdt.spb.ru/spektakli/privideniya/',
        datetime=datetime.datetime(2023, 6, 8, 19, 00)
    )
