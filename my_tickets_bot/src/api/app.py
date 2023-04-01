from urllib import parse

from asyncpg import Connection
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from services.calendar import generate_icalendar_content
from services.config import load_config
from services.repositories import Repo
from .consts import ORIGINS
from .database import Database
from .models import Parser, ParserDetails

config = load_config()
app = FastAPI()

db = Database(load_config())
CONTENT_TYPE = 'text/calendar'

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


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


@app.get('/api/parsers/')
async def get_parsers(repo: Repo = Depends(get_repository)) -> list[Parser]:
    """Получение доступных парсеров"""
    records = await repo.parser.list()
    return [Parser(**raw_parser) for raw_parser in records]


@app.get('/api/parsers/{parser_id}/')
async def get_pasers(
        parser_id: int,
        repo: Repo = Depends(get_repository),
) -> ParserDetails:
    """Получение подробной информации о парсере"""
    record = await repo.parser.get(parser_id)
    if not record:
        raise HTTPException(404, 'Not found')

    return ParserDetails(**record)
