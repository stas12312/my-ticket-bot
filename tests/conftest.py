"""Общие фикстуры"""
import asyncio

import asyncpg
import pytest
import pytest_asyncio
from asyncpg.transaction import Transaction

from services.repositories import Repo


@pytest_asyncio.fixture(scope='session')
async def conn() -> asyncpg.Connection:
    """Подключение к БД"""
    pool: asyncpg.Pool = await asyncpg.create_pool("postgresql://postgres:postgres@localhost:6432/test?sslmode=disable")
    connection: asyncpg.Connection = await pool.acquire()
    transaction: Transaction = connection.transaction()
    await transaction.start()
    yield connection
    await transaction.rollback()


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# pylint: disable=redefined-outer-name
@pytest_asyncio.fixture(scope='session')
async def repo(conn: asyncpg.Connection) -> Repo:
    """Создание репозитория"""
    return Repo(conn)
