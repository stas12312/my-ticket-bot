"""Модель место проведения"""
import dataclasses

from .city import City


@dataclasses.dataclass
class Place:
    """Модель места проведения"""
    place_id: int
    name: str
    address: str
    city: City | None

    def get_show_text(self) -> str:
        """Формирования строки для отображения"""
        return f'{self.name} ({self.city.name}, {self.address})'
