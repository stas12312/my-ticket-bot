"""Вспомогательные функции для сообщений"""

from aiogram.utils.text_decorations import markdown_decoration


def quote(
        value: str
) -> str:
    """Экранирование"""
    return markdown_decoration.quote(value)


TIME_EXAMPLES = f'Примеры:\n' \
                f'_{quote("20.03.23 20:00")}_\n' \
                f'_{quote("20.03 19:00")}_\n' \
                f'_{quote("20 марта 21:30")}_'


def make_message_by_rows(
        rows: list[str],
) -> str:
    """Формирование сообщения из списка строк"""
    return '\n'.join(rows)
