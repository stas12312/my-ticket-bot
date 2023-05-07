import datetime

import pytz
from dateutil.relativedelta import relativedelta

from services.event_time import set_year


class DateUtilsMixin:
    """Утилиты для работы с датами"""

    @classmethod
    def get_now(
            cls,
            shift: int = 0,
            timezone: str = 'UTC',
    ) -> datetime.datetime:
        """Получение текущей даты для определения полной даты и времени"""
        pytz_timezone = pytz.timezone(timezone)
        now = datetime.datetime.now(tz=pytz_timezone) - relativedelta(days=1)
        if shift:
            return now - relativedelta(days=1)
        return now

    @classmethod
    def set_year_by_date(
            cls,
            date: datetime.date,
            shift: int = 0,
            timezone: str = pytz.UTC,
    ) -> datetime.date:
        """Установка года по дате"""
        now = DateUtilsMixin.get_now(shift=shift, timezone=timezone)
        return set_year(date, now)

    @classmethod
    def set_year_by_day_and_month(
            cls,
            day: int,
            month: int,
            shift: int = 0,
            timezone: str = 'UTC',
    ) -> datetime.date:
        """Установка даты по дню и месяцу"""
        date = datetime.date(1, month, day)
        now = DateUtilsMixin.get_now(shift=shift, timezone=timezone)
        return set_year(date, now)
