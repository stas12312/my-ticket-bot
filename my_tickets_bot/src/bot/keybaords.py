"""Клавиатуры"""

from aiogram.utils.keyboard import (
    ReplyKeyboardMarkup,
    ReplyKeyboardBuilder,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardBuilder,
)

from models import City, Location, Event, Ticket
from .buttons import (
    MainMenu,
    Settings,
    Action,
)
from .callbacks import (
    CityCallback,
    EntityAction,
    PlaceCallback,
    SettingsCallback,
    CloseCallback,
    TicketCallback,
    EventCallback,
)

CLOSE_BUTTON = InlineKeyboardButton(
    text=Settings.CLOSE,
    callback_data=CloseCallback().pack(),
)


def get_menu_keyboard() -> ReplyKeyboardMarkup:
    """Получение клавиатуры для меню"""
    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text=MainMenu.MY_EVENTS), KeyboardButton(text=MainMenu.ADD_EVENT))
    builder.row(KeyboardButton(text=MainMenu.SETTINGS))

    return builder.as_markup(resize_keyboard=True)


def get_keyboard_by_values(
        values: list[str],
) -> ReplyKeyboardMarkup:
    """Получение клавиатуры"""
    builder = ReplyKeyboardBuilder()

    for value in values:
        builder.row(KeyboardButton(text=value))

    return builder.as_markup(resize_keyboard=True)


def get_settings_menu() -> InlineKeyboardMarkup:
    """Получение клавиатуры для настроек"""
    builder = InlineKeyboardBuilder()
    print(CityCallback(action=EntityAction.list).pack())
    builder.row(
        InlineKeyboardButton(
            text=Settings.MY_CITIES,
            callback_data=CityCallback(action=EntityAction.list).pack(),
        ),
        InlineKeyboardButton(
            text=Settings.MY_PLACES,
            callback_data=PlaceCallback(action=EntityAction.list).pack()
        ),
    )
    builder.row(CLOSE_BUTTON)

    return builder.as_markup()


def get_cities_menu(
        cities: list[City]
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для выбора города"""
    builder = InlineKeyboardBuilder()

    for city in cities:
        builder.row(
            InlineKeyboardButton(
                text=city.name,
                callback_data=CityCallback(action=EntityAction.show, city_id=city.city_id).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=Settings.ADD_CITY,
            callback_data=CityCallback(action=EntityAction.add).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=SettingsCallback(action=EntityAction.show).pack(),
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
            text=Settings.DELETE_CITY,
            callback_data=CityCallback(action=EntityAction.delete, city_id=city_id).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=CityCallback(action=EntityAction.list).pack(),
        ),
        CLOSE_BUTTON,
    )

    return builder.as_markup()


def get_places_menu(
        locations: list[Location],
) -> InlineKeyboardMarkup:
    """Получение меню для списка мест"""
    builder = InlineKeyboardBuilder()

    for location in locations:
        builder.row(
            InlineKeyboardButton(
                text=location.get_show_text(),
                callback_data=PlaceCallback(action=EntityAction.show, place_id=location.location_id).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=Settings.ADD_LOCATION,
            callback_data=PlaceCallback(action=EntityAction.add).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=SettingsCallback(action=EntityAction.show).pack(),
        ),
        CLOSE_BUTTON,
    )

    return builder.as_markup()


def get_actions_for_location(
        place_id: int,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для действия с местом"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=Settings.DELETE_LOCATION,
            callback_data=PlaceCallback(action=EntityAction.delete, city_id=place_id).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=PlaceCallback(action=EntityAction.list).pack(),
        ),
        CLOSE_BUTTON,
    )

    return builder.as_markup()


def get_actions_for_event(
        event: Event,
        tickets: list[Ticket],
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для события"""
    builder = InlineKeyboardBuilder()

    for row, ticket in enumerate(tickets, start=1):
        builder.row(
            InlineKeyboardButton(
                text=f'⬇ Билет {row}',
                callback_data=TicketCallback(action=EntityAction.show, ticket_id=ticket.ticket_id).pack(),
            )
        )

    builder.row(
        CLOSE_BUTTON,
        InlineKeyboardButton(
            text=Action.DELETE,
            callback_data=EventCallback(action=EntityAction.delete, event_id=event.event_id).pack(),
        )
    )

    return builder.as_markup()
