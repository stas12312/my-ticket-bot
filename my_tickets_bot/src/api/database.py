import asyncpg
from asyncpg import Pool, Connection

from services.config import Config


class Database:
    """БД для API"""

    def __init__(self, config: Config):
        self.pool: Pool | None = None
        self.config = config

    async def create_pool(self):
        """Создание пула подключения к Postgres"""
        self.pool = await asyncpg.create_pool(
            dsn=self.config.get_dsn(),
        )

    async def get_session(self) -> Connection:
        """Получение сессии"""
        connection: Connection
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                yield connection
