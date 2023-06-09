"""Модель место проведения"""
import dataclasses

from .city import City


@dataclasses.dataclass
class Location:
    """Модель места проведения"""
    location_id: int
    name: str | None = None
    address: str | None = None
    city: City | None = None
    url: str | None = None
