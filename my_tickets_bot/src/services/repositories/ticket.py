import datetime

import asyncpg

from models import Ticket, Place, User, City
from .queries import ticket as query


class TicketRepo:
    """Репозиторий билета"""

    def __init__(
            self,
            connection: asyncpg.Connection,
    ):
        self._conn = connection

    async def save(
            self,
            user_id: int,
            place_id: int,
            event_name: str,
            event_time: datetime.datetime,
            event_link: str,
            file_id: int,
    ):
        """Сохранение билета"""

        raw_ticket = await self._conn.fetchrow(
            query.SAVE_TICKET, user_id, place_id, event_time, event_name, file_id, event_link,
        )

        return Ticket(
            ticket_id=raw_ticket['id'],
            created_at=raw_ticket['created_at'],
            event_time=raw_ticket['event_time'],
            user=User(user_id=raw_ticket['user_id']),
            place=Place(place_id=raw_ticket['place_id']),
            event_link=raw_ticket['event_link'],
            event_name=raw_ticket['event_name'],
            file_url='',
        )

    async def list(
            self,
            user_id: int,
    ) -> list[Ticket]:
        """Список билетов пользователя"""

        raw_tickets = await self._conn.fetch(query.GET_TICKETS, user_id)

        tickets: list[Ticket] = []
        for ticket in raw_tickets:
            tickets.append(_convert_record_to_ticket(ticket))
        return tickets


def _convert_record_to_ticket(record: asyncpg.Record) -> Ticket:
    """Конвертация рекорда в модель"""
    return Ticket(
        ticket_id=record['ticket_id'],
        created_at=record['created_at'],
        event_time=record['event_time'],
        event_name=record['event_name'],
        user=User(
            user_id=record['user_id'],
        ),
        place=Place(
            place_id=record['place_id'],
            name=record['place_name'],
            address=record['place_address'],
            city=City(
                city_id=record['city_id'],
                name=record['city_name'],
                timezone=record['timezone_name'],
            ),
        ),
        event_link=record['event_link'],
        file_url=record['file_location'],
    )
