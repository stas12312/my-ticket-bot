import dataclasses
import datetime
from uuid import UUID

from .location import Location
from .user import User


@dataclasses.dataclass
class Event:
    """Модель события"""
    event_id: int
    name: str
    time: datetime.datetime
    location: Location
    link: str | None = None
    user: User | None = None
    uuid: UUID | None = None
