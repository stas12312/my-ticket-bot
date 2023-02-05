from asyncpg import Connection, Record

from .queries import user


class UserRepo:
    """Репозиторий для пользователя"""

    def __init__(
            self,
            connection: Connection,
    ):
        self._conn = connection

    async def save(
            self,
            user_id: int,
            username: str | None,
    ) -> Record:
        """Сохранение пользователя"""
        return await self._conn.fetchrow(user.SAVE_USER, user_id, username)
