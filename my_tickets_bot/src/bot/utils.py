"""Вспомогательные функции"""
from enum import IntEnum

from aiogram.types import File


class FileType(IntEnum):
    PHOTO = 0
    DOCUMENT = 1


def get_file_type(
        file: File,
) -> FileType:
    """Определение типа файла"""
    if file.file_path.startswith('documents'):
        return FileType.DOCUMENT
    return FileType.PHOTO
