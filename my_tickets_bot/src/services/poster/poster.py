import dataclasses
import datetime
import logging
import traceback

import aiogram
import asyncpg

from services.poster import Event
from services.poster.parsers import WebParser
from services.poster.sql import REGISTER_PARSER, GET_PARSERS_BY_DATETIME
from services.poster.utils import get_db_events, save_events, calc_new_events
from services.profile import duration


@dataclasses.dataclass
class ParserResult:
    """Результат парсинга"""
    parser: WebParser
    events: list[Event]


class Poster:
    """
    Класс для работы с афишами театров
    и уведомлением пользователей о новых мероприяитй
    """

    def __init__(
            self,
            poll: asyncpg.Pool,
            parsers: list[WebParser],
            bot: aiogram.Bot,
    ):
        self._pool = poll
        self._parsers = parsers
        self._parser_by_name = {parser.name: parser for parser in parsers}
        self._bot = bot

    @duration
    async def register_parsers(self):
        """Регистрация всех парсеров"""
        for parser in self._parsers:
            await self._register_parser(parser)

    async def _register_parser(
            self,
            parser: WebParser,
    ):
        """Регистрация парсера в БД"""
        name = parser.__class__.__name__
        async with self._pool.acquire() as conn:
            await conn.fetch(REGISTER_PARSER, name, parser.config.url, parser.config.timezone)

    async def get_matched_parsers(
            self,
            conn: asyncpg.Connection,
            timestamp: datetime.datetime,
    ) -> list[WebParser]:
        """Получение парсеров, которые подходят по времени"""
        conn: asyncpg.Connection
        parser_names = await conn.fetchval(GET_PARSERS_BY_DATETIME, timestamp)
        return [self._parser_by_name[name] for name in parser_names]

    # pylint: disable=broad-except
    async def _get_events_for_parsers(
            self,
            conn: asyncpg.Connection,
            parsers: list[WebParser],
    ) -> list[ParserResult]:
        """Получение новых событий для парсеров"""
        result: list[ParserResult] = []
        for parser in parsers:
            try:
                parse_result = await self._get_new_events_for_parser(conn, parser)
                if parse_result.events:
                    result.append(parse_result)
            except Exception as exp:
                logging.error('Не удалось получить события для %s %s', parser.name, exp)
                logging.error(traceback.format_exc())

        return result

    @classmethod
    async def _get_new_events_for_parser(
            cls,
            conn: asyncpg.Connection,
            parser: WebParser,
    ) -> ParserResult:
        """Получение новых мероприятий для парсера"""
        db_events = await get_db_events(conn, parser)
        events = await parser.get_events()
        new_events = calc_new_events(db_events, events)
        await save_events(conn, parser, events)

        return ParserResult(
            parser=parser,
            events=new_events,
        )

    async def get_parsers_events(
            self,
            now: datetime.datetime,
    ) -> list[ParserResult]:
        """Получение новых мероприятий по времени"""
        async with self._pool.acquire() as conn:
            parsers = await self.get_matched_parsers(conn, now)
            return await self._get_events_for_parsers(conn, parsers)
