"""Репозиторий пользователя"""
from asyncpg import Connection

from models import User
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
            first_name: str | None,
            last_name: str | None,
    ) -> User:
        """Сохранение пользователя"""
        record = await self._conn.fetchrow(user.SAVE_USER, user_id, username, first_name, last_name)
        return _convert_record_to_user(record)


def _convert_record_to_user(record) -> User:
    """Преобразование рекорда в пользователя"""
    return User(
        user_id=record['id'],
        username=record['username'],
    )
