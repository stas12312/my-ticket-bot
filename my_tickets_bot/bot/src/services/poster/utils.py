import datetime
import json
from json import loads

import asyncpg

from services.poster import Event
from services.poster.parsers import WebParser
from services.poster.sql import GET_EVENTS_FOR_PARSER, SAVE_EVENTS_FOR_PARSER


async def get_db_events(
        conn: asyncpg.Connection,
        parser: WebParser) -> list[Event]:
    """Получение мероприятий из БД"""
    raw_events = loads(await conn.fetchval(GET_EVENTS_FOR_PARSER, parser.name))
    return json_to_events(raw_events)


async def save_events(
        conn: asyncpg.Connection,
        parser: WebParser,
        events: list[Event],
) -> None:
    """Сохранение мероприятий в БД"""
    json_events = events_to_json(events)
    await conn.fetch(SAVE_EVENTS_FOR_PARSER, parser.name, json.dumps(json_events), datetime.datetime.utcnow())


def calc_new_events(
        db_events: list[Event],
        events: list[Event],
) -> list[Event]:
    """Получение новых событий"""
    new_events: list[Event] = []
    for event in events:
        if event not in db_events:
            new_events.append(event)

    return new_events


def json_to_events(
        raw_events: list[dict],
) -> list[Event]:
    """Преобразование JSON-а в мероприятия"""
    events: list[Event] = []
    for raw_event in raw_events:
        events.append(Event(
            datetime=datetime.datetime.fromisoformat(raw_event['datetime']),
            name=raw_event['name'],
            url=raw_event['url'],
        ))
    return events


def events_to_json(
        events: list[Event],
) -> list[dict]:
    """Преобразование мероприятий в JSON"""
    json_events = []
    for event in events:
        json_events.append({
            'datetime': event.datetime.isoformat(),
            'name': event.name,
            'url': event.url
        })
    return json_events
