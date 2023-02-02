"""Модель место проведения"""
import dataclasses

from .city import City


@dataclasses.dataclass
class Place:
    """Модель места проведения"""
    place_id: int
    name: str
    city: City
