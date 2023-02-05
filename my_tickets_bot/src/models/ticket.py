"""Модель билета"""
import dataclasses
from datetime import datetime

from .place import Place
from .user import User


@dataclasses.dataclass
class Ticket:
    """Модель билета"""
    ticket_id: int
    created_at: datetime
    event_time: datetime
    event_name: str
    user: User
    place: Place
    event_link: str
    file_url: str
