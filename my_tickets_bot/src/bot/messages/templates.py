from .utils import quote

DATETIME_EXAMPLES = f'Примеры:\n' \
                    f'_{quote("20.03.23 20:00")}_\n' \
                    f'_{quote("20.03 19:00")}_\n' \
                    f'_{quote("20 марта 21:30")}_'

DATE_EXAMPLES = f'Примеры:\n' \
                f'_{quote("20.03.23")}_\n' \
                f'_{quote("20.03")}_\n' \
                f'_{quote("20 марта")}_'

DURATION_EXAMPLES = f'Примеры:\n' \
                    f'_{quote("30 - количество минут")}_\n' \
                    f'_{quote("1:30 - количество часов и минут")}_\n'
