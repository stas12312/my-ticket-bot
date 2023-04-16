import datetime

from bs4 import Tag, BeautifulSoup

from services.event_time import parse_date
from services.poster import Event
from services.poster.parsers import RequestData, HTMLBaseParser
from services.poster.parsers.web import Page, Config


class RedTorchParser(HTMLBaseParser):
    """Парсер для театра Красный факел"""

    def _get_elements(self, page: Page) -> list[Event]:
        data: BeautifulSoup = page.data
        block_by_date = data.findAll('div', {'class': 'playbill-list-new__item'})
        events: list[Event] = []
        for block in block_by_date:
            date_div = block.find('div', {'class': 'playbill-list-new__item-date'})
            raw_date = date_div.text.strip().split('·')[0]
            date = parse_date(raw_date, datetime.datetime.utcnow())

            elements = block.findAll('div', {'class': 'playbill-list-new__item-content'})
            events.extend([self._element_to_event(element, date) for element in elements])
        return events

    def _element_to_event(self, element: Tag, date: datetime.date) -> Event:
        """Преобразование элемента в событие"""
        raw_time = element.find('div', {'class': 'playbill-list-new__item-desc__text'}).find('strong').text
        time = datetime.time.fromisoformat(raw_time)
        description = element.find('a', {'class': 'playbill-list-new__item-desc__link'})

        name = ' '.join(description.text.replace('\n', '').split())
        url = description['href']

        return Event(
            name=name,
            url=self.build_url(self.config.url, url),
            datetime=datetime.datetime.combine(date, time),
        )

    @classmethod
    def get_config(cls) -> Config:
        return Config(
            url='https://red-torch.ru/',
            timezone='Asia/Novosibirsk',
        )

    def _get_page_params(self, number: int) -> RequestData | None:
        if number > 0:
            return None

        return RequestData(
            url=self.config.url,
        )
