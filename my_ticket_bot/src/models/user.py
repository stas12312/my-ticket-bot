"""Модель пользователя"""
import dataclasses
from datetime import datetime


@dataclasses.dataclass
class User:
    """Модель пользователя"""
    user_id: int
    username: str
    created_at: datetime
    phone: str
