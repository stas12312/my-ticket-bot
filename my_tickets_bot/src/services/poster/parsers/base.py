import abc

from services.poster import Event


class BaseParser(abc.ABC):
    """Базовый класс стратегии для парсинга афиш театров"""

    @abc.abstractmethod
    async def get_events(self) -> list[Event]:
        """Получение мероприятий"""
