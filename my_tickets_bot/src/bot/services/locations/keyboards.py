from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons import Settings
from bot.callbacks import LocationCallback, EntityAction, CityCallback
from bot.keybaords import CLOSE_BUTTON
from models import Location


def get_locations_menu(
        city_id: int,
        locations: list[Location],
) -> InlineKeyboardMarkup:
    """Получение меню для списка мест"""
    builder = InlineKeyboardBuilder()

    for location in locations:
        builder.row(
            InlineKeyboardButton(
                text=location.name,
                callback_data=LocationCallback(action=EntityAction.SHOW, location_id=location.location_id).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=Settings.ADD_LOCATION,
            callback_data=LocationCallback(action=EntityAction.ADD, city_id=city_id).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=CityCallback(action=EntityAction.SHOW, city_id=city_id).pack(),
        ),
        CLOSE_BUTTON,
    )

    return builder.as_markup()


def get_actions_for_location(
        city_id: int,
        location_id: int,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для действия с местом"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=Settings.DELETE_LOCATION,
            callback_data=LocationCallback(
                action=EntityAction.DELETE,
                city_id=city_id,
                location_id=location_id
            ).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=LocationCallback(action=EntityAction.LIST, city_id=city_id).pack(),
        ),
        CLOSE_BUTTON,
    )

    return builder.as_markup()
