"""Обработка даты и времени мероприятия"""
import datetime

import pytz

DATETIME_FORMATS = [
    '%d.%m.%Y %H:%M',
    '%d.%m.%Y %H %M',
    '%d.%m.%y %H:%M',
    '%d.%m.%y %H %M',
]


def parse_datetime(
        raw_datetime: str,
        timezone_name: str,
) -> datetime.datetime | None:
    """Парсинг введённой даты"""

    if (parsed_datetime := convert(raw_datetime)) is None:
        return None

    # Если ввели год из двух цифр
    if parsed_datetime.year < 2000:
        parsed_datetime = parsed_datetime.replace(year=parsed_datetime.year + 2000)

    return parsed_datetime.replace(tzinfo=pytz.timezone(timezone_name))


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
