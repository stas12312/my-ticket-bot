"""Тесты работы со временем события"""
import datetime

import pytest

from services.event_time import get_beatify_datetime, get_left_time

testdata = [
    (6, 2, 23, 14, 10, '6 Февраля в 14:10 (Пн)'),
    (7, 8, 22, 9, 2, '7 Августа в 9:02 (Вс)'),
]


@pytest.mark.parametrize('day,month,year,hour,minute,result', testdata)
def test_beautify_datetime(day: int, month: int, year: int, hour: int, minute: int, result):
    """Проверка преобразования даты в красивый вид"""
    datetime_ = datetime.datetime(year, month, day, hour, minute)

    beautify_time = get_beatify_datetime(datetime_)
    assert beautify_time == result


testdata = [
    (datetime.datetime(2022, 2, 1, 14, 30), datetime.datetime(2023, 4, 3, 15, 30), '1 год 2 месяца'),
    (datetime.datetime(2022, 4, 3, 15, 30), datetime.datetime(2023, 4, 3, 15, 30), '1 год'),
    (datetime.datetime(2023, 1, 1, 14, 30), datetime.datetime(2023, 4, 3, 15, 30), '3 месяца 2 дня'),
    (datetime.datetime(2023, 1, 3, 14, 30), datetime.datetime(2023, 4, 3, 15, 30), '3 месяца'),
    (datetime.datetime(2023, 4, 2, 10, 15), datetime.datetime(2023, 4, 3, 15, 30), '1 день 5 часов'),
    (datetime.datetime(2023, 4, 2, 15, 15), datetime.datetime(2023, 4, 3, 15, 30), '1 день'),
    (datetime.datetime(2023, 4, 3, 14, 00), datetime.datetime(2023, 4, 3, 15, 30), '1 час 30 минут'),
    (datetime.datetime(2023, 4, 3, 14, 30), datetime.datetime(2023, 4, 3, 15, 30), '1 час'),
    (datetime.datetime(2023, 4, 3, 15, 19), datetime.datetime(2023, 4, 3, 15, 30), '11 минут'),
    (datetime.datetime(2023, 4, 5, 15, 15), datetime.datetime(2023, 4, 3, 15, 30), None),
]


@pytest.mark.parametrize('first,second,result', testdata)
def test_get_interval(first: datetime.datetime, second: datetime.datetime, result: str):
    """Проверка получения оставшегося времени"""
    assert get_left_time(first, second) == result
