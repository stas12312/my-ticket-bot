import datetime

from bs4 import Tag, BeautifulSoup

from services.poster import Event
from services.poster.parsers import RequestData, HTMLBaseParser
from services.poster.parsers.web import Page, Config


class GlobusParser(HTMLBaseParser):
    """Парсер для театра ГЛОБУС"""

    def _get_page_params(self, number: int) -> RequestData | None:
        if number > 0:
            return None
        return RequestData(
            self.build_url(self.config.url, 'afisha'),
        )

    def _get_elements(self, page: Page) -> list[Event]:
        data: BeautifulSoup = page.data
        items = data.find('div', {'class': 'playbill__items'})

        return [self._element_to_event(element) for element in items.find_all('div', {'class': 'playbill__item'})]

    def _element_to_event(self, element: Tag) -> Event:
        """Преобразование элемента в событие"""
        date = datetime.date.fromisoformat(element['data-date'])
        time = datetime.time.fromisoformat(element.find('div', {'class': 'playbill__item-time'}).text)
        url = element.find('a', {'class': 'playbill__item-name'})['href']
        name = element.find('div', {'class': 'playbill__item-name__value'}).text

        return Event(
            name=name,
            url=self.build_url(self.config.url, url),
            datetime=datetime.datetime.combine(date, time),
        )

    @classmethod
    def get_config(cls) -> Config:
        return Config(
            url='https://globus-nsk.ru/',
            timezone='Asia/Novosibirsk',
        )
