"""Тесты работы со временем события"""
import datetime

import pytest

from services.event_time import get_beatify_datetime

testdata = [
    (6, 2, 23, 14, 10, '6 Февраля в 14:10 (Пн)'),
    (7, 8, 22, 9, 20, '7 Августа в 9:20 (Вс)'),
]


@pytest.mark.parametrize('day,month,year,hour,minute,result', testdata)
def test_beautify_datetime(day: int, month: int, year: int, hour: int, minute: int, result):
    """Проверка преобразования даты в красивый вид"""
    dt = datetime.datetime(year, month, day, hour, minute)

    beautify_time = get_beatify_datetime(dt)
    assert beautify_time == result
