from aiogram.utils.markdown import bold

from services.statistic import RowStatistic


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
