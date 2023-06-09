import abc
from math import ceil


class BasePaginator(abc.ABC):
    """Базовый класс для пагинации"""

    def __init__(
            self,
            number: int,
            size: int,
    ):
        self.size = size
        self.number = number
        self.total: int | None = None

    async def has_next(self) -> bool:
        """Получение флага наличия следующей страницы"""
        return self.number < (await self.get_page_count() - 1)

    async def has_prev(self):
        """Получение флага наличия предыдущей страницы"""
        return self.number > 0

    def prev_page(self) -> int:
        """Предыдущая страница"""
        return self.number - 1

    def next_page(self) -> int:
        """Следующая страница"""
        return self.number + 1

    def get_offset(self) -> int:
        """Получение сдвига"""
        return self.number * self.size

    async def get_page_count(self) -> int:
        """Получение количества страниц"""
        return ceil(await self.get_total() / self.size)

    @abc.abstractmethod
    async def get_total(self) -> int:
        """Получение количества записей"""

    @abc.abstractmethod
    async def get_data(self) -> list:
        """Получение данных со страницы"""
