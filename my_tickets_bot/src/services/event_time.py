"""Обработка даты и времени мероприятия"""
import datetime

import pytz

DATETIME_FORMATS = [
    '%d.%m.%Y %H:%M',
    '%d.%m.%Y %H %M',
    '%d.%m.%y %H:%M',
    '%d.%m.%y %H %M',
]

MONTH_TO_NAME = [
    'Января',
    'Февраля',
    'Марта',
    'Апреля',
    'Мая',
    'Июня',
    'Июля',
    'Августа',
    'Сентября',
    'Октября',
    'Ноября',
    'Декабря',
]

DAY_TO_NAME = [
    'Пн',
    'Вт',
    'Ср',
    'Чт',
    'Пт',
    'Сб',
    'Вс',
]


def parse_datetime(
        raw_datetime: str,
        timezone_name: str,
) -> datetime.datetime | None:
    """Парсинг введённой даты"""

    if (parsed_datetime := convert(raw_datetime)) is None:
        return None

    timezone = pytz.timezone(timezone_name)

    parsed_datetime = timezone.localize(parsed_datetime)

    return parsed_datetime


def get_beatify_datetime(
        dt: datetime.datetime,
) -> str:
    """Получение строки для даты и времени"""
    month_name = MONTH_TO_NAME[dt.month]
    day_name = DAY_TO_NAME[dt.weekday()]
    return f'{dt.day} {month_name} в {dt.hour}:{dt.minute} ({day_name})'



def convert(
        raw_datetime: str,
) -> datetime.datetime | None:
    """Конвертация в дату"""
    for fmt in DATETIME_FORMATS:
        try:
            return datetime.datetime.strptime(raw_datetime, fmt)
        except ValueError:
            pass

    return None
