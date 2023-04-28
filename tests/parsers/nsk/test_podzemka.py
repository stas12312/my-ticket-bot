import datetime
import os
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

import pytest

from parsers.nsk import PodzemkaNskParser


# pylint: disable=unused-argument
def get_data(url: str, params: dict, headers: dict | None = None) -> str:
    """Получение страницы"""

    if params['PAGEN_1'] == 1:
        path = Path(os.path.dirname(os.path.realpath(__file__)), 'files/podzemka-1.html')
        with path.open(encoding='UTF-8') as file:
            return file.read()

    if params['PAGEN_1'] == 2:
        path = Path(os.path.dirname(os.path.realpath(__file__)), 'files/podzemka-2.html')
        with path.open(encoding='UTF-8') as file:
            return file.read()

    return ''


@pytest.mark.asyncio
async def test_podzemka_parser():
    """Проверка парсера для Поздемки"""
    parser = PodzemkaNskParser()

    parser.get_now = MagicMock(return_value=datetime.datetime(2023, 1, 1))
    parser.get_data_from_url = AsyncMock(side_effect=get_data)

    events = await parser.get_events()
    assert len(events) == 4

    first_event = events[0]
    assert first_event.name == 'Yung Nation #54'
    assert first_event.url == 'https://podzemka.site/catalog/2221/'
    assert first_event.datetime == datetime.datetime(2023, 5, 1, 17, 30)

    second_event = events[1]
    assert second_event.name == 'Thomas Mra'
    assert second_event.url == 'https://podzemka.site/catalog/2201/'
    assert second_event.datetime == datetime.datetime(2023, 5, 3, 20, 0)

    third_event = events[2]
    assert third_event.name == 'План Ломоносова'
    assert third_event.url == 'https://podzemka.site/catalog/2223/'
    assert third_event.datetime == datetime.datetime(2023, 10, 19, 20, 0)

    forth_event = events[3]
    assert forth_event.name == 'Дельфин'
    assert forth_event.url == 'https://podzemka.site/catalog/2197/'
    assert forth_event.datetime == datetime.datetime(2023, 11, 23, 19, 0)
