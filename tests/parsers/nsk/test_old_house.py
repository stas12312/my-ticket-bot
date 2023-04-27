import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from parsers.nsk import OldHouseParser
from parsers.nsk.old_house import QUERY_TEMPLATE


# pylint: disable=unused-argument
def get_data(url: str, params: dict, headers: dict) -> str:
    """Получение страницы"""

    if params['z'] == QUERY_TEMPLATE.format(month='Апрель', year=2023):
        with open('files/old-house-1.json', encoding='UTF-8') as file:
            return file.read()

    if params['z'] == QUERY_TEMPLATE.format(month='Май', year=2023):
        with open('files/old-house-2.json', encoding='UTF-8') as file:
            return file.read()

    return '{"cont": ""}'


@pytest.mark.asyncio
async def test_old_house_parser():
    """Проверка парсера для театра Старый Дом"""
    parser = OldHouseParser()
    parser.get_data_from_url = AsyncMock(side_effect=get_data)
    parser.get_now = MagicMock(return_value=datetime.datetime(2023, 4, 1, 0, 0))

    events = await parser.get_events()
    assert len(events) == 4

    first_event = events[0]
    assert first_event.name == 'Анна Каренина'
    assert first_event.url == 'https://old-house.ru/anna-karenina.html'
    assert first_event.datetime == datetime.datetime(2023, 4, 14, 18, 30)

    second_event = events[1]
    assert second_event.name == 'Анна Каренина'
    assert second_event.url == 'https://old-house.ru/anna-karenina.html'
    assert second_event.datetime == datetime.datetime(2023, 4, 15, 18, 00)

    third_event = events[2]
    assert third_event.name == 'Остановка'
    assert third_event.url == 'https://old-house.ru/ostanovka.html'
    assert third_event.datetime == datetime.datetime(2023, 5, 4, 18, 30)

    forth_event = events[3]
    assert forth_event.name == 'Вишневый сад'
    assert forth_event.url == 'https://old-house.ru/vishnevyj-sad.html'
    assert forth_event.datetime == datetime.datetime(2023, 5, 5, 18, 30)
