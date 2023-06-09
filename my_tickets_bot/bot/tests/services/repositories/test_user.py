"""Тесты репозитория пользователя"""
import asyncpg
import pytest

from services.repositories.user import UserRepo


@pytest.mark.asyncio
async def test_create_user(
        conn: asyncpg.Connection,
        user_repo: UserRepo,
):
    """Проверка добавления пользователя"""

    await user_repo.save(100, 'username', 'first_name', 'last_name')
    user_in_db = await conn.fetchrow('SELECT * FROM "user" WHERE id=100')
    assert user_in_db['username'] == 'username'
    assert user_in_db['first_name'] == 'first_name'
    assert user_in_db['last_name'] == 'last_name'
    assert user_in_db['id'] == 100
