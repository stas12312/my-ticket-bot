"""Модель пользователя"""
import dataclasses
from datetime import datetime


@dataclasses.dataclass
class User:
    """Модель пользователя"""
    user_id: int
    username: str | None = None
    created_at: datetime | None = None
    first_name: str | None = None
    last_name: str | None = None
