"""Фикстуры для тестов репозиториев"""
import asyncpg
import pytest

from services.repositories.user import UserRepo


@pytest.fixture(scope='session')
def user_repo(conn: asyncpg.Connection) -> UserRepo:
    """Репозиторий пользователя"""
    return UserRepo(conn)
