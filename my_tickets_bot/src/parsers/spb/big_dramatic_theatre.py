import datetime

from bs4 import BeautifulSoup, Tag

from services.event_time import set_year
from services.poster import Event
from services.poster.parsers import HTMLBaseParser, RequestData
from services.poster.parsers.web import Config, Page


class BigDramaticTheaterSpb(HTMLBaseParser):
    """Парсер для Большого Драматического Театра"""

    def _get_elements(self, page: Page) -> list[Event]:
        data: BeautifulSoup = page.data

        events: list[Event] = []
        for block in data.findAll('div', {'class': 'afisha-row'})[1:]:
            events.extend(self._get_events_from_block(block))
        return events

    def _get_events_from_block(self, block: Tag) -> list[Event]:
        """Получение событий из строки"""
        date_block = block.find('div', {'class': 'cell-date'}).find('span')
        day, month = [int(v) for v in date_block.text.strip().split('/')]
        date = datetime.date(1, month, day)
        date = set_year(date, self.get_now(shift=1))
        events: list[Event] = []
        for row in block.find('div', {'class': 'cell-data'}).findAll('div', recursive=False):
            event = self._get_event_from_row(date, row)
            if event:
                events.append(event)
        return events

    def _get_event_from_row(self, date: datetime.date, row: Tag) -> Event | None:
        """Получение события из строки"""
        name_element = row.find('div', {'class': 'cell-name'})
        link_element = name_element.find('a', recursive=False) or name_element.find('a', recursive=True)
        if not link_element:
            return None
        url = link_element['href']
        name = link_element.text.strip()
        time_element = row.find('em')
        raw_time = time_element.text.split()[-1]
        time = datetime.time.fromisoformat(raw_time)

        return Event(
            url=self.build_url(self.config.url, url),
            name=name,
            datetime=datetime.datetime.combine(date, time),
        )

    async def _get_page_params(self, number: int) -> RequestData | None:
        if number == 0:
            return RequestData(url=self.build_url(self.config.url, 'afisha'))

        index = number - 1
        urls = await self._get_page_urls()
        if index >= len(urls):
            return None
        url = urls[index]
        return RequestData(url=self.build_url(self.config.url, url))

    async def _get_page_urls(self) -> list[str]:
        """Получение ссылок на страницы"""
        if 'page_urls' not in self._cache:
            self._cache['page_urls'] = await self._parse_page_urls()

        return self._cache['page_urls']

    async def _parse_page_urls(self) -> list[str]:
        """Парсинг страницы для получения пагинации"""
        request_data = RequestData(
            url=self.build_url(self.config.url, 'afisha'),
        )
        data = await self._get_prepared_data_from_url(request_data)
        menu = data.find('ul', {'class': 'dirmenu'})
        urls = []
        for url_item in menu.findAll('a'):
            url = url_item['href']
            if 'month' in url:
                urls.append(url)
        return urls

    @classmethod
    def get_config(cls) -> Config:
        return Config(
            url='https://bdt.spb.ru/',
            timezone='Europe/Moscow',
        )
