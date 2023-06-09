from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ButtonType

from bot.buttons import Settings, Pagination
from bot.callbacks import CloseCallback, PaginationCallback
from services.paginator import BasePaginator


def get_keyboard_by_values(
        values: list[str],
) -> ReplyKeyboardMarkup:
    """Получение клавиатуры"""
    builder = ReplyKeyboardBuilder()

    for value in values:
        builder.row(KeyboardButton(text=value))

    return builder.as_markup(resize_keyboard=True)


CLOSE_BUTTON = InlineKeyboardButton(
    text=Settings.CLOSE,
    callback_data=CloseCallback().pack(),
)


def get_back_and_close_row(
        callback_data: CallbackData,

) -> tuple[InlineKeyboardButton, InlineKeyboardButton]:
    """Получение строки с кнопками Назад и Закрыть"""
    back_btn = InlineKeyboardButton(
        text=Settings.BACK,
        callback_data=callback_data.pack(),
    )

    return back_btn, CLOSE_BUTTON


async def get_pagination_buttons(
        mode: int,
        paginator: BasePaginator,
        object_name: str,
) -> list[ButtonType]:
    """Формирование строки пагинации"""
    prev_page = paginator.prev_page() if await paginator.has_prev() else None
    next_page = paginator.next_page() if await paginator.has_next() else None

    return [
        InlineKeyboardButton(
            text=Pagination.PREV if prev_page is not None else ' ',
            callback_data=PaginationCallback(
                object_name=object_name,
                page=prev_page,
                mode=mode,
            ).pack(),
        ),
        InlineKeyboardButton(
            text=f'{paginator.number + 1} / {await paginator.get_page_count()}',
            callback_data=PaginationCallback(
                object_name=object_name,
            ).pack(),
        ),
        InlineKeyboardButton(
            text=Pagination.NEXT if next_page is not None else ' ',
            callback_data=PaginationCallback(
                object_name=object_name,
                page=next_page,
                mode=mode,
            ).pack(),
        ),
    ]
