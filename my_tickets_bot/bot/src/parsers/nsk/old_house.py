import datetime

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

from services.event_time import MONTH_TO_NAME
from services.poster import Event
from services.poster.parsers import JsonParser
from services.poster.parsers.web import RequestData, Page, Config

QUERY_TEMPLATE = '{month}<sub>{year}</sub>'


class OldHouseParser(JsonParser):
    """Парсер для старого дома"""

    async def _get_page_params(self, number: int) -> RequestData | None:
        date = get_month_by_shift(number)

        url = self.build_url(self.config.url, 'assets/modules/calendar/ajax/rep_return.php')
        params = {
            'z': QUERY_TEMPLATE.format(month=MONTH_TO_NAME[date.month - 1], year=date.year)
        }

        return RequestData(
            url=url,
            params=params,
            metadata={
                'date': date,
            }
        )

    def _get_elements(self, page: Page) -> list[Event]:
        data = page.data
        content = data['cont']
        html_bs = BeautifulSoup(content, 'lxml')
        # Преобразовываем HTML в dict
        elements = html_bs.findAll('div', {'class': 'elem'})
        date = page.metadata.get('date')
        return [self._element_to_event(element, date) for element in elements]

    def _element_to_event(self, element: BeautifulSoup, date: datetime.date) -> Event:
        """Преобразование элемента в событие"""
        url = element.find('a')['href']
        name = element.find('a').text
        day = int(element.find('h2').find('span').text)
        raw_time = element.find('h3').text
        time = datetime.time.fromisoformat(raw_time)
        date_with_day = date.replace(day=day)
        return Event(
            datetime=datetime.datetime.combine(date_with_day, time),
            name=name,
            url=self.build_url(self.config.url, url, with_slash=False),
        )

    @classmethod
    def get_config(cls) -> Config:
        return Config(
            url='https://old-house.ru/',
            timezone='Asia/Novosibirsk',
        )


def get_month_by_shift(
        shift: int
) -> datetime.date:
    """Получение месяца по сдвигу от текущей даты"""
    now = JsonParser.get_now()

    return now + relativedelta(months=shift)
