import dataclasses

from models.file import File


@dataclasses.dataclass
class Ticket:
    """Модель билета"""
    ticket_id: int
    file: File
    comment: str | None = None
