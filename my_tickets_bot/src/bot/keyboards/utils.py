from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.buttons import Settings
from bot.callbacks import CloseCallback


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
