import dataclasses
import datetime


@dataclasses.dataclass
class Event:
    """Событие для парсера"""
    datetime: datetime.datetime
    name: str
    url: str
