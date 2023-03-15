"""Обработка даты и времени мероприятия"""
import datetime
import re

import pytz

from .localization import plural

DATETIME_FORMATS = [
    '%d.%m.%Y %H:%M',
    '%d.%m.%Y %H %M',
    '%d.%m.%y %H:%M',
    '%d.%m.%y %H %M',
    '%d.%m %H:%M',
]

DATE_FORMATS = [
    '%d.%m',
    '%d.%m',
    '%d.%m.%y',
]

DATETIME_REGEX = re.compile(r'^([1-3]?[0-9]) (\w*) ([0-2][0-9]:[0-9][0-9])')
DATE_REGEX = re.compile(r'^([1-3]?[0-9]) (\w*)')

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

MONTH_NAME_TO_NUMBER = {name: number for number, name in enumerate(MONTH_TO_NAME, start=1)}

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
        input_value: str,
        timezone_name: str | None = None,
        now: datetime.datetime | None = None,
) -> datetime.datetime | None:
    """Парсинг введённой даты"""

    if (parsed_datetime := convert(input_value, DATETIME_FORMATS)) is None:
        return None

    if now:
        parsed_datetime = set_year(parsed_datetime, now)
    return localize_datetime(parsed_datetime, timezone_name) if timezone_name else parsed_datetime


def parse_date(
        input_value: str,
        now: datetime.datetime | None = None,
) -> datetime.date | None:
    """Парсинг введённой даты"""
    if (parsed_date := convert(input_value, DATE_FORMATS)) is None:
        return None

    if now:
        parsed_date = set_year(parsed_date, now)

    return parsed_date


def set_year(
        datetime_: datetime.datetime | datetime.date,
        now: datetime.datetime,
) -> datetime.datetime:
    """Определение года"""
    if datetime_.year >= now.year:
        return datetime_

    if datetime_.month * 31 + datetime_.day < now.month * 31 + now.day:
        return datetime_.replace(year=now.year + 1)
    return datetime_.replace(year=now.year)


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
        formats: list[str],
) -> datetime.datetime | None:
    """Конвертация в дату"""
    for fmt in formats:
        try:
            return datetime.datetime.strptime(raw_datetime, fmt)
        except ValueError:
            pass

    return convert_datetime_with_month(raw_datetime) or convert_date_with_month(raw_datetime)


def convert_datetime_with_month(
        raw_datetime: str,
) -> datetime.datetime | None:
    """Конвертация строки с названием месяца в дату"""
    result = DATETIME_REGEX.match(raw_datetime)
    if not result:
        return None

    day = result.group(1)
    month_name = result.group(2).capitalize()
    hour, minute = result.group(3).split(':')

    month_number = MONTH_NAME_TO_NUMBER.get(month_name)
    if month_number is None:
        return None

    try:
        return datetime.datetime(datetime.MINYEAR, month_number, int(day), int(hour), int(minute))
    except ValueError:
        return None


def convert_date_with_month(
        row_date: str,
) -> datetime.date | None:
    """Конвертация даты с введенными названием месяца"""
    result = DATE_REGEX.match(row_date)
    if not result:
        return None

    day = result.group(1)
    month_name = result.group(2).capitalize()

    month_number = MONTH_NAME_TO_NUMBER.get(month_name)
    if month_number is None:
        return None

    try:
        return datetime.date(datetime.MINYEAR, month_number, int(day))
    except ValueError:
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


def get_localtime(timezone: str) -> datetime.datetime:
    """Получение локального времени во временной зоне"""
    now = datetime.datetime.utcnow()
    return pytz.utc.localize(now).astimezone(pytz.timezone(timezone))
