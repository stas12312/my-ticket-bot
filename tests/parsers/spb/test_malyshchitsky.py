import datetime
import os
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

import pytest

from parsers.spb import MalyshchitskyParserSpb


@pytest.mark.asyncio
async def test_malyshchitsky_parser():
    """Проверка парсера"""
    parser = MalyshchitskyParserSpb()
    parser.get_now = MagicMock(return_value=datetime.datetime(2023, 1, 1))

    path = Path(os.path.dirname(os.path.realpath(__file__)), 'files/malyshchitsky.html')
    with path.open(encoding='UTF-8') as file:
        parser.get_data_from_url = AsyncMock(return_value=file.read())

    events = await parser.get_events()

    assert len(events) == 2
