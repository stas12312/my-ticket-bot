import dataclasses


@dataclasses.dataclass
class Ticket:
    """Модель билета"""
    ticket_id: int
    file_url: str
    comment: str | None = None
