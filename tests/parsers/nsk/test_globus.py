from unittest.mock import AsyncMock

import pytest

from parsers.nsk import GlobusParser


@pytest.mark.asyncio
async def test_globus_parser():
    """Проверка парсера для театра Глобус"""
    with open('files/globus.html', encoding='UTF-8') as file:
        html = file.read()

    parser = GlobusParser()
    parser.get_data_from_url = AsyncMock(return_value=html)
    events = await parser.get_events()
    assert len(events) == 2

    first_event = events[0]
    assert first_event.url == 'https://globus-nsk.ru/spektakli/cabaret/'
    assert first_event.name == 'Cabaret'

    second_event = events[1]
    assert second_event.url == 'https://globus-nsk.ru/spektakli/art/'
    assert second_event.name == 'Art'
