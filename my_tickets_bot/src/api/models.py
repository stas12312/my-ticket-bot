import datetime

from pydantic import BaseModel


class Parser(BaseModel):
    """Модель парсера для API"""
    name: str
    events_count: int | None
    timestamp: datetime.datetime | None
    timezone: str
    url: str


class Event(BaseModel):
    """Модель события"""
    name: str
    url: str
    datetime: str


class ParserDetails(Parser):
    """Модель парсера с расширенной информацией"""
    events: list[Event] | None
