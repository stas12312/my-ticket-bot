"""Фикстуры для тестов репозиториев"""
import asyncpg
import pytest
import pytest_asyncio

from models import User, City, Location
from services.repositories import Repo
from services.repositories.common import CommonRepo
from services.repositories.user import UserRepo


@pytest.fixture(scope='session')
def user_repo(conn: asyncpg.Connection) -> UserRepo:
    """Репозиторий пользователя"""
    return UserRepo(conn)


@pytest.fixture(scope='session')
def common_repo(conn: asyncpg.Connection) -> CommonRepo:
    """Репозиторий общих запросов"""
    return CommonRepo(conn)


@pytest.fixture(scope='session')
def repo(conn: asyncpg.Connection) -> Repo:
    """Основной репозиторий"""
    return Repo(conn)


# pylint: disable=redefined-outer-name
@pytest_asyncio.fixture(scope='session')
async def user(repo: Repo) -> User:
    """Пользователь"""
    return await repo.user.save(1, 'username', 'first_name', 'last_name')


# pylint: disable=redefined-outer-name
@pytest_asyncio.fixture(scope='session')
async def city(repo: Repo) -> City:
    """Город"""
    return await repo.city.create(1, 'Moscow', 'Europe/Moscow')


# pylint: disable=redefined-outer-name
@pytest_asyncio.fixture(scope='session')
async def location(repo: Repo, city: City) -> Location:
    """Локация"""
    return await repo.location.save(city.city_id, 'location', 'address')
