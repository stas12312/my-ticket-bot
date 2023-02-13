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

    return localize_datetime(parsed_datetime, timezone_name)


def localize_datetime(
        datetime_: datetime.datetime,
        timezone_name: str,
) -> datetime.datetime:
    """Локализация времени"""
    timezone = pytz.timezone(timezone_name)

    return timezone.localize(datetime_)


def get_beatify_datetime(
        datetime_: datetime.datetime,
) -> str:
    """Получение строки для даты и времени"""
    month_name = MONTH_TO_NAME[datetime_.month - 1]
    day_name = DAY_TO_NAME[datetime_.weekday()]
    return f'{datetime_.day} {month_name} в {datetime_.hour}:{datetime_.minute:02d} ({day_name})'


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
