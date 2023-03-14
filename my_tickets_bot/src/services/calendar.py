"""Работа с событием в календаре"""
import io
from datetime import timedelta, datetime

from icalendar import Calendar, Event as CEvent, vText

from bot.messages.event import make_message_for_calendar
from models import Event

CONTENT_TYPE = 'text/calendar'


def generate_icalendar_content(
        event: Event,
) -> Calendar:
    """Формирование события для календаря"""
    location = event.location
    calendar = Calendar()
    calendar.add('prodid', '-//stas12312//MyTicketsBot//RU')
    calendar.add('version', '2.0')

    c_event = CEvent()
    c_event.add('dtstart', event.time)
    # Пока что по умолчанию ставим 1 час
    c_event.add('dtend', event.time + timedelta(hours=1))
    c_event.add('dtstamp', datetime.utcnow())
    c_event.add('summary', f'{event.name}')
    c_event.add('location', vText(location.name))

    c_event.add('description ', vText(make_message_for_calendar(event)))

    calendar.add_component(c_event)

    return calendar


def get_calendar_for_event(
        event: Event,
) -> io.BytesIO:
    """Формирование файла календаря"""
    calendar = generate_icalendar_content(event)
    return io.BytesIO(calendar.to_ical())
