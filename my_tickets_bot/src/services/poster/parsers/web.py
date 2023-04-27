import abc
import dataclasses
import datetime
from typing import Any

from aiogram.client.session import aiohttp
from dateutil.relativedelta import relativedelta

from .base import BaseParser
from .. import Event


@dataclasses.dataclass
class RequestData:
    """Параметры для запрос"""
    url: str | None = None
    params: dict | None = None
    headers: dict | None = None
    metadata: dict | None = None


@dataclasses.dataclass
class Page:
    """Информация о странице"""
    data: Any
    metadata: dict[str, Any]


@dataclasses.dataclass
class Config:
    """Конфигурация парсера"""
    url: str
    timezone: str


class WebParser(BaseParser, abc.ABC):
    """Стратегия для парсинга сайтов"""

    def __init__(self):
        self.need_next_page = True

    async def get_events(self) -> list[Event]:
        return await self.get_all_elements()

    async def get_all_elements(self) -> list[Event]:
        """Получение всех элементов с афиши"""
        items = []
        number = 0
        while True:
            page = await self.get_page(number)
            if not page:
                break
            page_items = self._get_elements(page)
            if not page_items:
                break
            items.extend(page_items)
            if not self.need_next_page:
                break
            number += 1
        return items

    async def get_page(
            self,
            number: int,
    ) -> Page | None:
        """Получение страницы"""
        request_data = self._get_page_params(number)
        if not request_data:
            return None

        data = await self._get_prepared_data_from_url(request_data)
        return Page(
            data=data,
            metadata=request_data.metadata,
        )

    @abc.abstractmethod
    def _get_elements(self, page: Page) -> list[Event]:
        """Получение элементов"""

    @abc.abstractmethod
    def _get_page_params(
            self,
            number: int,
    ) -> RequestData | None:
        """Получение параметров для страницы"""

    @classmethod
    async def get_data_from_url(
            cls,
            url: str,
            params: dict | None = None,
            headers: dict | None = None,
    ) -> str:
        """Получение содержимого по URL"""
        async with aiohttp.ClientSession() as session:
            if headers:
                session.headers.extend(headers)
            async with session.get(url, params=params) as resp:
                return await resp.text()

    @classmethod
    def build_url(cls, *parts: str, with_slash: bool = True):
        """Формирование URL"""
        url = '/'.join([part.strip('/') for part in parts])
        return url if url[-1] == '/' or not with_slash else f'{url}/'

    @abc.abstractmethod
    async def _get_prepared_data_from_url(
            self,
            request_data: RequestData,
    ) -> Any:
        """Получение подготовленных данных"""

    @property
    def config(self) -> Config:
        """Получение таймзоны"""
        return self.get_config()

    @classmethod
    @abc.abstractmethod
    def get_config(cls) -> Config:
        """Получение конфигурации парсера"""

    @property
    def name(self) -> str:
        """Название парсера"""
        return self.__class__.__name__

    @staticmethod
    def get_now(shift: int = 0) -> datetime.datetime:
        """Получение текущей даты для определения полной даты и времени"""
        now = datetime.datetime.utcnow() - relativedelta(days=1)
        if shift:
            return now - relativedelta(days=1)
        return now
