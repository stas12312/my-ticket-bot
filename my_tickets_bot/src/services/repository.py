"""Класс для работы с БД"""
import logging
from typing import Optional

from asyncpg import Connection, Record

from . import sql

logger = logging.getLogger(__name__)


class Repo:

    def __init__(
            self,
            connection: Connection,
    ):
        self._conn = connection

    async def save_user(
            self,
            user_id: int,
            username: Optional[str],
    ) -> Record:
        """Сохранение пользователя"""
        logger.info('Сохранение пользователя')
        return await self._conn.fetchrow(sql.SAVE_USER, user_id, username)
