import datetime

from aiohttp import hdrs
from bs4 import BeautifulSoup, Tag, ResultSet

from services.event_time import MONTH_TO_NAME
from services.poster import Event
from services.poster.parsers import HTMLBaseParser, RequestData
from services.poster.parsers.web import Config, Page


class AlexandrinskySpb(HTMLBaseParser):
    """Парсер для Александрийского театра"""

    def _get_elements(self, page: Page) -> list[Event]:
        data: BeautifulSoup = page.data
        event_block = data.findAll('div', {'class': 'box-poster-tickets'})
        events = []
        # На первой странице приходит общее количество страниц
        total_page = data.find('input', {'id': 'all-page'})
        if total_page:
            self._cache['total_page'] = int(total_page['value'])
        for block in event_block:
            events.extend(self._get_element_for_block(block))
        return events

    def _get_element_for_block(
            self,
            block: Tag,
    ) -> list[Event]:
        """Получение событий из блока мероприятия"""
        event_rows = self._get_html_rows_from_block(block)
        if not event_rows:
            return []
        events = []
        name = block.find('h4').text
        url_postfix = block.find('h4').find('a')['href']
        url = self.build_url(self.config.url, url_postfix)
        for row in event_rows:
            link_block = row.find('a')
            block_elements = link_block.findAll('span')
            day = int(block_elements[0].text)
            month_name: str = block_elements[1].text
            month = [n + 1 for n, m in enumerate(MONTH_TO_NAME) if m.startswith(month_name.capitalize())][0]
            raw_time = block_elements[2].text
            time = datetime.time.fromisoformat(raw_time)
            date = self.set_year_by_day_and_month(day, month, timezone=self.config.timezone)
            events.append(
                Event(
                    datetime=datetime.datetime.combine(date, time),
                    name=name,
                    url=url,
                )
            )
        return events

    @classmethod
    def _get_html_rows_from_block(
            cls,
            block: Tag,
    ) -> ResultSet | None:
        """Получение набора событий"""
        container = (
                block.find('ul', {'class': 'repertoire-date-list clearfix box-all-dates'})
                or block.find('ul', {'class': 'repertoire-date-list clearfix box-five-dates'})
        )
        return container.findAll('li') if container else None

    async def _get_page_params(self, number: int) -> RequestData | None:
        # Параметр заполнится после парсинга первой страницы
        total_page = self._cache.get('total_page')
        if total_page and number > total_page:
            return None

        return RequestData(
            url=self.build_url(self.config.url, 'afisha-i-bilety'),
            params={
                'ajax_request': 'y',
                'PAGEN_2': number,
            },
            method=hdrs.METH_POST,
        )

    @classmethod
    def get_config(cls) -> Config:
        return Config(
            url='https://alexandrinsky.ru/',
            timezone='Europe/Moscow',
        )
