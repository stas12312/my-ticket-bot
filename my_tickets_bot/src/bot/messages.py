"""Формирование красивых сообщений"""

from aiogram.utils.markdown import bold
from aiogram.utils.text_decorations import markdown_decoration

from services.statistic import RowStatistic


def quote(
        value: str
) -> str:
    """Экранирование"""
    return markdown_decoration.quote(value)


TIME_EXAMPLES = f'Примеры:\n' \
                f'_{quote("20.03.23 20:00")}_\n' \
                f'_{quote("20.03 19:00")}_\n' \
                f'_{quote("20 марта 21:30")}_'


def _make_message_by_rows(
        rows: list[str],
) -> str:
    """Формирование сообщения из списка строк"""
    return '\n'.join(rows)


def get_message_for_statistic(
        statistic: list[RowStatistic],
) -> str:
    """Формирование сообщения для статистики"""
    total_count = 0
    rows = ['📊 Статистика мероприятий 📊']
    for row in statistic:
        rows.append(f'\n{bold(row.year)}')
        if row.past_count:
            rows.append(f'Прошедшие: {row.past_count}')
        if row.planned_count:
            rows.append(f'Планируются: {row.planned_count}')
        total_count += row.planned_count + row.past_count

    return '\n'.join(rows)
