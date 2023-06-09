import datetime

from bs4 import BeautifulSoup, Tag

from services.event_time import MONTH_TO_NAME_FOR_TEXT, set_year
from services.poster import Event
from services.poster.parsers import HTMLBaseParser, RequestData
from services.poster.parsers.web import Config, Page


class MalyshchitskyParserSpb(HTMLBaseParser):
    """Парсер для Камерного театра Малыщицкого"""

    def _get_elements(self, page: Page) -> list[Event]:
        data: BeautifulSoup = page.data
        items = data.findAll('div', {'class': 't396__artboard'})[2:-3]
        return [self._item_to_element(item) for item in items]

    def _item_to_element(self, raw_item: Tag) -> Event:
        """Преобразование в элемент"""
        text_items = raw_item.findAll('div', {'data-elem-type': 'text'})
        day = int(text_items[0].text)
        raw_time = text_items[1].text.strip()
        name = text_items[2].text.strip()
        month_name = text_items[5].text.strip().capitalize()
        time = datetime.time.fromisoformat(raw_time)
        date_without_year = datetime.date(1, MONTH_TO_NAME_FOR_TEXT.index(month_name) + 1, day)
        date = set_year(date_without_year, self.get_now())
        url = raw_item.find('a')['href']
        return Event(
            datetime=datetime.datetime.combine(date, time),
            name=name,
            url=self.build_url(self.config.url, url, with_slash=False),
        )

    async def _get_page_params(self, number: int) -> RequestData | None:
        # Без пагинации
        if number > 0:
            return None

        return RequestData(
            self.build_url(self.config.url, 'afisha', with_slash=False),
        )

    @classmethod
    def get_config(cls) -> Config:
        return Config(
            url='https://www.vmtheatre.ru/',
            timezone='Europe/Moscow',
        )
