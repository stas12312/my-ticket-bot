import pytest

from bot.utils import MAX_LENGTH, split_long_message

testdata = [
    '0123456789\n',
    '0123456789'
]


@pytest.mark.parametrize('message', testdata)
def test_split_log_message(message):
    """Проверка разделения длинного сообщения"""
    parts_for_limit = MAX_LENGTH // len(message)
    long_message = message * parts_for_limit * 2

    result = split_long_message(long_message)
    assert len(result) == 2
    assert len(result[0]) <= MAX_LENGTH
    assert len(result[1]) <= MAX_LENGTH


def test_split_short_message():
    """Проверка разделения короткого сообщения"""
    message = 'Test string'
    result = split_long_message(message)
    assert len(result) == 1
    assert result[0] == message
