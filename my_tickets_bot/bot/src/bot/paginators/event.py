import datetime

from models import Event
from services.paginator import BasePaginator
from services.repositories import Repo


class EventPaginator(BasePaginator):
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
        super().__init__(
            number=number,
            size=size,
        )
        self.user_id = user_id
        self.is_actual = is_actual
        self.actual_datetime = actual_datetime
        self.size = size
        self.repo = repo

    async def get_total(self) -> int:
        if self.total is None:
            self.total = await self.repo.event.get_count(self.user_id, self.is_actual, self.actual_datetime)
        return self.total

    async def get_data(self) -> list[Event]:
        """Получение событий"""
        return await self.repo.event.list(
            user_id=self.user_id,
            is_actual=self.is_actual,
            actual_time=self.actual_datetime,
            offset=self.number * self.size,
            limit=self.size,
            asc=self.is_actual,
        )
