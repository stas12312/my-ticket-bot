from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons import Settings
from bot.callbacks import CityCallback, EntityAction
from bot.keyboards.utils import CLOSE_BUTTON


def get_settings_menu() -> InlineKeyboardMarkup:
    """Получение клавиатуры для настроек"""
    builder = InlineKeyboardBuilder()
    print(CityCallback(action=EntityAction.LIST).pack())
    builder.row(
        InlineKeyboardButton(
            text=Settings.CITIES_AND_PLACES,
            callback_data=CityCallback(action=EntityAction.LIST).pack(),
        ),
    )
    builder.row(CLOSE_BUTTON)

    return builder.as_markup()
