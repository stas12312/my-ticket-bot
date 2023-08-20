"""Работа с событием в календаре"""
from datetime import timedelta
from urllib import parse

from models import Event

CONTENT_TYPE = 'text/calendar'

URL_TEMPLATE = 'https://calendar.google.com/calendar/render?{params}'
TIME_FORMAT = '%Y%m%dT%H%M%SZ'


def get_url_for_google_calendar(
        event: Event,
) -> str:
    """Формирование URL для Google календаря"""
    params = {
        'action': 'TEMPLATE',
        'text': parse.quote_plus(event.name),
        'details': parse.quote_plus(make_description(event)),
        'dates': make_dates(event),
        'location': parse.quote_plus(event.location.name),
    }

    url_params = '&'.join(f'{name}={value}' for name, value in params.items())
    return URL_TEMPLATE.format(params=url_params)


def make_dates(
        event: Event,
) -> str:
    """Формирование строки даты"""
    end_time = event.end_time if event.end_time else event.time + timedelta(hours=1)

    return f'{event.time.strftime(TIME_FORMAT)}/{end_time.strftime(TIME_FORMAT)}'


def make_description(
        event: Event,
) -> str:
    """Формирование описания"""
    rows = [
        f'📍 {event.location.city.name}, {event.location.name}'
    ]
    if event.link:
        rows.append(f'🔗 {event.link}')

    return '\n'.join(rows)
