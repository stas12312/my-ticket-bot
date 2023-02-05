"""Формирование красивых сообщений"""
import datetime

from aiogram.utils.markdown import bold, link
from aiogram.utils.text_decorations import markdown_decoration as mark

from models import Ticket


def make_ticket_message(
        ticket: Ticket,
        with_command: bool = False,
) -> str:
    """Формирование сообщения для описания билета"""

    event_link = link(ticket.event_name, ticket.event_link)

    rows = [
        f'🎟 Билет на *{event_link}*',
        f'📍 {mark.bold(ticket.place.name)} _{mark.quote(ticket.place.city.name)} {mark.quote(ticket.place.address)}_',
        f'🕚 {bold(beatify_date(ticket.event_time))}',
    ]

    if with_command:
        command = mark.quote(f'/ticket_{ticket.ticket_id}')
        rows.append(f'⚙ Управлять билетом: {command}')

    return '\n'.join(rows)


def beatify_date(raw_datetime: datetime.datetime) -> str:
    """Преобразование даты в корректное представление"""

    return raw_datetime.strftime('%d.%m.%Y %H:%M')
