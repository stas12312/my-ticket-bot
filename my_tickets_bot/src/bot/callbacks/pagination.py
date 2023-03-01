from aiogram.filters.callback_data import CallbackData


class PaginationCallback(CallbackData, prefix='page'):
    """CallbackData для пагинации"""
    object_name: str
    page: int | None
