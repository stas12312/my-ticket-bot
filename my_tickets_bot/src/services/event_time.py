"""Обработка даты и времени мероприятия"""
import datetime

import pytz

from .localization import plural

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

SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = 1
MONTH = 30
YEAR = MONTH * 12


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


def get_left_time(
        first: datetime.datetime,
        second: datetime.datetime,
) -> str | None:
    """
    Получение оставшегося времени между двумя временными точками
    Имеют значение только две соседние пары времен
    """
    delta = second - first

    if delta.total_seconds() < 0:
        return None

    # Считаем все значения
    minutes, _ = divmod(delta.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    months, days = divmod(delta.days, 30)
    years, months = divmod(months, 12)

    # Формируем строки с правильным окончанием
    names = [
        plural(years, 'год', 'года', 'лет'),
        plural(months, 'месяц', 'месяца', 'месяцев'),
        plural(days, 'день', 'дня', 'дней'),
        plural(hours, 'час', 'часа', 'часов'),
        plural(minutes, 'минута', 'минуты', 'минут')
    ]
    main_parts = [years, months, days, hours, minutes]
    additional_parts = [months, days, hours, minutes, None]

    for i, (main_part, additional_part) in enumerate(zip(main_parts, additional_parts)):
        if main_part and additional_part:
            return f'{names[i]} {names[i + 1]}'
        if main_part:
            return f'{names[i]}'

    return None
