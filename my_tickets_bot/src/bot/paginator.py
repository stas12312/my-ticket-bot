"""Пагинация"""
import datetime

from math import ceil

from models import Event
from services.repositories import Repo


class EventPaginator:
    """Пагинация для мероприятий"""

    def __init__(
            self,
            user_id: int,
            is_actual: bool,
            actual_datetime: datetime.datetime,
            number: int,
            size: int,
            repo: Repo,
    ):
        self.user_id = user_id
        self.is_actual = is_actual
        self.actual_datetime = actual_datetime
        self.page = number
        self.size = size
        self.repo = repo
        self.total_count = None

    async def has_next(self) -> bool:
        """Получение флага наличия следующей страницы"""
        return self.page < (await self.get_page_count() - 1)

    def prev_page(self) -> int:
        """Предыдущая страница"""
        return self.page - 1

    def next_page(self) -> int:
        """Следующая страница"""
        return self.page + 1

    async def has_prev(self):
        """Получение флага наличия предыдущей страницы"""
        return self.page > 0

    async def get_count(self) -> int:
        """Получение количества записей"""
        if self.total_count is None:
            self.total_count = await self.repo.event.get_count(self.user_id, self.is_actual, self.actual_datetime)
        return self.total_count

    async def get_page_count(self) -> int:
        """Получение общего количества страниц"""
        return ceil(await self.get_count() / self.size)

    def get_offset(self) -> int:
        """Получение сдвига"""
        return self.page * self.size

    async def get_events(self) -> list[Event]:
        """Получение событий"""
        return await self.repo.event.list(
            user_id=self.user_id,
            is_actual=self.is_actual,
            actual_time=self.actual_datetime,
            offset=self.page * self.size,
            limit=self.size,
            asc=self.is_actual,
        )
