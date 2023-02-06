"""Модель файла"""
import dataclasses


@dataclasses.dataclass
class File:
    """Модель файла"""
    file_id: int
    ticket_id: int
    location: str
