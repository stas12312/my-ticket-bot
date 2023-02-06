"""Тестирование работы с Emoji"""
import datetime

import pytest

from bot.emoji import get_interval_number

testdata = [
    (0, 14, 0),
    (0, 29, 1),
    (0, 30, 1),
    (12, 00, 0),
    (12, 10, 0),
    (23, 59, 24),

]


@pytest.mark.parametrize('hour,minute,correct_interval', testdata)
def test_get_interval(hour: int, minute: int, correct_interval: str):
    time = datetime.time(hour=hour, minute=minute)

    interval = get_interval_number(time)

    assert interval == correct_interval
