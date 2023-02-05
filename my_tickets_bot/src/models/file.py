"""Модель файла"""
import dataclasses


@dataclasses.dataclass
class File:
    """Модель файла"""
    file_id: int
    location: str
    file_type: int
