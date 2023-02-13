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
    LocationCallback,
    SettingsCallback,
    CloseCallback,
    TicketCallback,
    EventCallback,
    EditEventCallback, EditEventField,
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
    print(CityCallback(action=EntityAction.LIST).pack())
    builder.row(
        InlineKeyboardButton(
            text=Settings.MY_CITIES,
            callback_data=CityCallback(action=EntityAction.LIST).pack(),
        ),
        InlineKeyboardButton(
            text=Settings.MY_PLACES,
            callback_data=LocationCallback(action=EntityAction.LIST).pack()
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
            text=Settings.DELETE_CITY,
            callback_data=CityCallback(action=EntityAction.DELETE, city_id=city_id).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=CityCallback(action=EntityAction.LIST).pack(),
        ),
        CLOSE_BUTTON,
    )

    return builder.as_markup()


def get_locations_menu(
        locations: list[Location],
) -> InlineKeyboardMarkup:
    """Получение меню для списка мест"""
    builder = InlineKeyboardBuilder()

    for location in locations:
        builder.row(
            InlineKeyboardButton(
                text=location.get_show_text(),
                callback_data=LocationCallback(action=EntityAction.SHOW, location_id=location.location_id).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=Settings.ADD_LOCATION,
            callback_data=LocationCallback(action=EntityAction.ADD).pack(),
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


def get_actions_for_location(
        location_id: int,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для действия с местом"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=Settings.DELETE_LOCATION,
            callback_data=LocationCallback(action=EntityAction.DELETE, location_id=location_id).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=LocationCallback(action=EntityAction.LIST).pack(),
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
                callback_data=TicketCallback(
                    action=EntityAction.SHOW,
                    ticket_id=ticket.ticket_id,
                    event_id=event.event_id,
                ).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=Action.ADD,
            callback_data=TicketCallback(action=EntityAction.ADD, event_id=event.event_id).pack(),
        )
    )

    builder.row(
        InlineKeyboardButton(
            text=Action.EDIT,
            callback_data=EventCallback(action=EntityAction.EDIT, event_id=event.event_id).pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text=Action.DELETE,
            callback_data=EventCallback(action=EntityAction.DELETE, event_id=event.event_id).pack(),
        ),
        CLOSE_BUTTON,
    )

    return builder.as_markup()


def get_actions_for_ticket(
        ticket: Ticket,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для билетов"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=Action.DELETE,
            callback_data=TicketCallback(
                action=EntityAction.DELETE,
                ticket_id=ticket.ticket_id,
            ).pack(),
        ),
        CLOSE_BUTTON,
    )

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


def get_actions_for_edit_event(
        event_id: int,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для редактирования события"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text='Изменить название',
            callback_data=EditEventCallback(
                field_name=EditEventField.NAME,
                event_id=event_id,
            ).pack(),
        ),
        InlineKeyboardButton(
            text='Изменить место',
            callback_data=EditEventCallback(
                field_name=EditEventField.LOCATION,
                event_id=event_id,
            ).pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text='Изменить время',
            callback_data=EditEventCallback(
                field_name=EditEventField.TIME,
                event_id=event_id,
            ).pack(),
        ),
        InlineKeyboardButton(
            text='Изменить ссылку',
            callback_data=EditEventCallback(
                field_name=EditEventField.LINK,
                event_id=event_id,
            ).pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text=Settings.BACK,
            callback_data=EventCallback(
                action=EntityAction.SHOW,
                event_id=event_id,
            ).pack(),
        ),
        CLOSE_BUTTON,
    )
    return builder.as_markup()
