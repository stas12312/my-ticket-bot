"""Модель города"""
import dataclasses


@dataclasses.dataclass
class City:
    """Модель города"""
    city_id: int
    name: str | None = None
    timezone: str | None = None
