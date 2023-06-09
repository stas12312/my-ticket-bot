from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons import Settings, Action
from bot.callbacks import CityCallback, EntityAction, SettingsCallback, LocationCallback
from bot.keyboards.utils import CLOSE_BUTTON, get_back_and_close_row
from models import City


def get_cities_menu(
        cities: list[City]
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для выбора города"""
    builder = InlineKeyboardBuilder()

    for city in cities:
        builder.row(
            InlineKeyboardButton(
                text=city.name,
                callback_data=CityCallback(action=EntityAction.SHOW, city_id=city.city_id).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=Settings.ADD_CITY,
            callback_data=CityCallback(action=EntityAction.ADD).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=SettingsCallback(action=EntityAction.SHOW).pack(),
        ),
        CLOSE_BUTTON,
    )

    return builder.as_markup()


def get_actions_for_city(
        city_id: int,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры с действиями для города"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=Settings.PLACES,
            callback_data=LocationCallback(action=EntityAction.LIST, city_id=city_id).pack()
        )
    )

    builder.row(
        InlineKeyboardButton(
            text=Action.EDIT,
            callback_data=CityCallback(action=EntityAction.EDIT, city_id=city_id).pack(),
        )
    )

    builder.row(*get_back_and_close_row(CityCallback(action=EntityAction.LIST)))
    return builder.as_markup()


def get_actions_for_edit(
        city_id: int,
) -> InlineKeyboardMarkup:
    """Действия для редактирования"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Settings.DELETE_CITY,
            callback_data=CityCallback(action=EntityAction.DELETE, city_id=city_id).pack(),
        )
    )
    builder.row(*get_back_and_close_row(CityCallback(action=EntityAction.SHOW, city_id=city_id)))
    return builder.as_markup()


def get_add_city_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для добавления города"""
    return InlineKeyboardBuilder([
        [
            InlineKeyboardButton(
                text=Settings.ADD_CITY,
                callback_data=CityCallback(
                    action=EntityAction.ADD,
                ).pack()
            ),
        ],
    ]).as_markup()
