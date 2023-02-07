import asyncpg

from models import Ticket
from models.file import File
from .queries import ticket as q


class TicketRepo:
    """Репозиторий билета"""

    def __init__(
            self,
            connection: asyncpg.Connection,
    ):
        self._conn = connection

    async def save(
            self,
            event_id: int,
            comment: str | None = None,
    ) -> Ticket:
        """Сохранение билета"""

        record = await self._conn.fetchrow(q.SAVE_TICKET, event_id, comment)

        return _convert_record_to_ticket(record)

    async def list_for_event(
            self,
            user_id: int,
            event_id: int,
    ) -> list[Ticket]:
        """Список билетов пользователя"""

        records = await self._conn.fetch(q.GET_TICKETS_FOR_EVENT, user_id, event_id)

        return [_convert_record_to_ticket(record) for record in records]

    async def get(
            self,
            user_id,
            ticket_id: int,
    ) -> Ticket:
        """Получение билета"""
        record = await self._conn.fetchrow(q.GET_TICKET_BY_ID, user_id, ticket_id)

        return _convert_record_to_ticket(record)


def _convert_record_to_ticket(
        record: asyncpg.Record,
) -> Ticket:
    """Конвертация рекорда в модель"""
    return Ticket(
        ticket_id=record.get('ticket_id'),
        comment=record.get('comment'),
        file=File(
            ticket_id=record.get('ticket_id'),
            file_id=record.get('file_id'),
            bot_file_id=record.get('bot_file_id'),
            location=record.get('file_location'),
        ),

    )
