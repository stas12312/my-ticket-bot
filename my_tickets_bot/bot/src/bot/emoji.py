import datetime
from math import floor

CLOCK_EMOJIS = [
    '🕛',  # 00:00
    '🕧',  # 00:30
    '🕑',  # 01:00
    '🕜',  # 01:30
    '🕑',  # 02:00
    '🕝',  # 02:30
    '🕒',  # 03:00
    '🕞',  # 03:30
    '🕓',  # 04:00
    '🕟',  # 04:30
    '🕔',  # 05:00
    '🕠',  # 05:30
    '🕕',  # 06:00
    '🕡',  # 06:30
    '🕖',  # 07:00
    '🕢',  # 07:30
    '🕗',  # 08:00
    '🕣',  # 08:30
    '🕘',  # 09:00
    '🕤',  # 09:30
    '🕙',  # 10:00
    '🕥',  # 10:30
    '🕚',  # 11:00
    '🕦',  # 11:30
    '🕛',  # 12:00
]

HR_12 = 60 * 12  # 12 часов в минутах


def get_clock_emoji(
        time: datetime.time | datetime.datetime,
) -> str:
    """Получение эмодзи часов в зависимости от времени"""

    interval = get_interval_number(time)
    return CLOCK_EMOJIS[interval]


def get_interval_number(
        time: datetime.time,
) -> int:
    """Получение номера интервала"""
    if (total_minutes := time.hour * 60 + time.minute) >= HR_12:
        total_minutes -= HR_12

    # Округляем к ближайшему интервалу
    return floor(total_minutes / 30 + 0.5)
