import datetime

from services.notifications.new_events import make_message
from services.poster import Event


def test_make_message_with_one():
    """Проверка формирования сообщения для одного события"""
    events = [Event(datetime=datetime.datetime(2023, 2, 2, 14, 00), name='Новое мероприятие', url='https://test.ru')]

    rows = make_message('Локация', events).split('\n')
    assert rows[0] == 'Новые мероприятия в Локация'
    assert rows[1] == '✨ *[Новое мероприятие](https://test.ru)*'
    assert rows[2] == '🕑 *2 Февраля в 14:00 \\(Чт\\)*'


def test_make_message_with_two():
    """Проверка формирования сообщения для двух событий"""
    events = [
        Event(datetime=datetime.datetime(2023, 2, 2, 14, 00), name='Новое мероприятие', url='https://test.ru'),
        Event(datetime=datetime.datetime(2023, 1, 2, 14, 00), name='Новое мероприятие 2', url='https://test2.ru'),
    ]
    rows = make_message('Локация', events).split('\n')
    assert rows[0] == 'Новые мероприятия в Локация'
    assert rows[1] == '✨ *[Новое мероприятие](https://test.ru)*'
    assert rows[2] == '🕑 *2 Февраля в 14:00 \\(Чт\\)*'
    assert rows[3] == ''
    assert rows[4] == '✨ *[Новое мероприятие 2](https://test2.ru)*'
    assert rows[5] == '🕑 *2 Января в 14:00 \\(Пн\\)*'
