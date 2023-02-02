"""Модель города"""
import dataclasses
from datetime import tzinfo


@dataclasses.dataclass
class City:
    """Модель города"""
    city_id: int
    name: str
    timezone: tzinfo
