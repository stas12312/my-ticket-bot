"""Работа с локализацией"""


def plural(
        number: int,
        *args,
) -> str:
    """Выбор окончания для числа"""
    word = args[2]
    if number % 10 in {2, 3, 4}:
        word = args[1]
    if number % 10 == 1 and number != 11:
        word = args[0]

    return f'{number} {word}'
