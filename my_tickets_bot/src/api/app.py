from urllib import parse

from asyncpg import Connection
from fastapi import FastAPI, Depends
from starlette.responses import Response

from services.calendar import generate_icalendar_content
from services.config import load_config
from services.repositories import Repo
from .database import Database

config = load_config()
app = FastAPI()

db = Database(load_config())
CONTENT_TYPE = 'text/calendar'


@app.on_event('startup')
async def startup():
    """Действия при запуске FastApi"""
    await db.create_pool()


async def get_repository(connection: Connection = Depends(db.get_session)) -> Repo:
    """Формирование репозитория"""
    return Repo(connection)


@app.get('/events/{event_uuid}/calendar-ics')
async def get_calendar_event(event_uuid: str, repo: Repo = Depends(get_repository)):
    """Получение данных для добавления события в календарь"""
    event_id = await repo.event.get_id_by_uuid(event_uuid)
    event = await repo.event.get(None, event_id)
    calendar = generate_icalendar_content(event)
    filename = parse.quote_plus(f'{event.name}.ics')
    headers = {
        'Content-Type': 'text/calendar',
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    return Response(
        content=calendar.to_ical(),
        headers=headers,
    )
