"""Middleware для создания подключения и сессии к бд"""
import logging
from typing import Awaitable, Any, Callable

from aiogram.types import Message
from asyncpg import Pool, Connection

from services.repositories import Repo

logger = logging.getLogger(__name__)


class DbMiddleware:
    """Создание подключения и сессии"""

    def __init__(
            self,
            poll: Pool,
    ):
        self.pool = poll

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any],
    ) -> Any:
        """
        Вызов обработчика
        Перед каждым обработчиком создаем соединение и сессию с БД,
        затем пробрасываем его в репозиторий
        """
        connection: Connection
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                data['repo'] = Repo(connection)
                return await handler(event, data)
