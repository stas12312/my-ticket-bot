import datetime

from bs4 import BeautifulSoup, Tag

from services.event_time import MONTH_TO_NAME_FOR_TEXT, set_year
from services.poster import Event
from services.poster.parsers import HTMLBaseParser, RequestData
from services.poster.parsers.web import Config, Page
from asyncio import sleep


class PodzemkaNskParser(HTMLBaseParser):
    """Парсер для Подземки"""

    def _get_elements(self, page: Page) -> list[Event]:
        # Делаем задержку, чтобы уменьшить частоту запросов
        sleep(1)
        data: BeautifulSoup = page.data
        items_container = data.find('ul', {'class': 'index__tab--active'})
        items = items_container.findAll('li', {'class': 'index__item'})
        # Определяем, что больше записей на странице нет
        refresh_container = items_container.find('div', {'class': 'refresh_container'})
        if refresh_container is None:
            self.need_next_page = False

        return [self._get_element(item) for item in items]

    def _get_element(self, raw_element: Tag) -> Event:
        """Получение элемента"""
        link = raw_element.find('a', {'class': 'index__item-title'})
        name = link.contents[0].text.strip()

        return Event(
            url=self.build_url(self.config.url, link['href']),
            name=name,
            datetime=get_datetime_from_element(raw_element),
        )

    def _get_page_params(self, number: int) -> RequestData | None:
        return RequestData(
            params={'PAGEN_1': number + 1},
            url=self.build_url(self.config.url)
        )

    @classmethod
    def get_config(cls) -> Config:
        return Config(
            url='https://podzemka.site/',
            timezone='Asia/Novosibirsk',
        )


def get_datetime_from_element(raw_element: Tag) -> datetime.datetime:
    """Получение даты и времени проведениямероприятия"""
    raw_time = raw_element.find('span', {'class': 'index__date-time'}).text.strip()
    date_span = raw_element.find('span', {'class': 'index__date'})
    day = date_span.find('strong').text.strip()
    month_name = date_span.contents[1].text.strip()
    raw_date = datetime.date(1, MONTH_TO_NAME_FOR_TEXT.index(month_name) + 1, int(day))
    time = datetime.time.fromisoformat(raw_time)

    now = HTMLBaseParser.get_now()
    date = set_year(raw_date, now)

    return datetime.datetime.combine(date, time)
