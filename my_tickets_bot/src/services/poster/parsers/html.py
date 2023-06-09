import abc

from bs4 import BeautifulSoup

from services.poster.parsers.web import WebParser, RequestData


class HTMLBaseParser(WebParser, abc.ABC):
    """Базовая стратегия для парсинга HTML-афиш"""

    async def _get_prepared_data_from_url(
            self,
            request_data: RequestData,
    ) -> BeautifulSoup:
        body = await self.get_data_from_url(request_data.url, request_data.params)
        return BeautifulSoup(body, 'lxml')
