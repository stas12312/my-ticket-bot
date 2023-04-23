import enum

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons import Action, Event as EventButton, Settings, Pagination
from bot.callbacks import TicketCallback, EntityAction, EventCallback, EditEventCallback, EditEventField, \
    PaginationCallback
from bot.keyboards.utils import CLOSE_BUTTON
from bot.paginator import EventPaginator
from models import Event, Ticket
from .common import get_url_button


class EventListMode(enum.Enum):
    """Режим отображения списка мероприятий"""
    PLANNED = enum.auto()
    PAST = enum.auto()


def get_actions_for_event(
        event: Event,
        tickets: list[Ticket],
        calendar_url: str | None = None
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для события"""
    builder = InlineKeyboardBuilder()

    if tickets:
        builder.row(
            InlineKeyboardButton(
                text='⬇ Билет' if len(tickets) == 1 else '⬇ Билеты',
                callback_data=TicketCallback(
                    action=EntityAction.SHOW,
                    event_id=event.event_id,
                ).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=Action.EDIT,
            callback_data=EventCallback(action=EntityAction.EDIT, event_id=event.event_id).pack(),
        ),
    )

    if calendar_url:
        builder.row(
            get_url_button(calendar_url, EventButton.ADD_IN_CALENDAR)
        )

    builder.row(
        CLOSE_BUTTON,
    )

    return builder.as_markup()


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
            text=EventButton.ADD_TICKET,
            callback_data=TicketCallback(action=EntityAction.ADD, event_id=event_id).pack(),
        )
    )

    builder.row(
        InlineKeyboardButton(
            text=Action.DELETE,
            callback_data=EventCallback(action=EntityAction.DELETE, event_id=event_id).pack(),
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


async def get_event_list_keyboard(
        event_paginator: EventPaginator,
        list_mode: EventListMode = EventListMode.PLANNED,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для списка мероприятий"""
    builder = InlineKeyboardBuilder()

    prev_page = event_paginator.prev_page() if await event_paginator.has_prev() else None
    next_page = event_paginator.next_page() if await event_paginator.has_next() else None

    builder.row(
        InlineKeyboardButton(
            text=EventButton.PAST if list_mode == EventListMode.PAST else EventButton.PLANNED,
            callback_data=PaginationCallback(
                object_name='EVENT',
                page=0,
                mode=EventListMode.PAST.value if list_mode == EventListMode.PLANNED else EventListMode.PLANNED.value
            ).pack()
        )
    )

    if await event_paginator.get_page_count() > 1:
        builder.row(
            InlineKeyboardButton(
                text=Pagination.PREV if prev_page is not None else ' ',
                callback_data=PaginationCallback(
                    object_name='EVENT',
                    page=prev_page,
                    mode=list_mode.value,
                ).pack(),
            ),
            InlineKeyboardButton(
                text=f'{event_paginator.page + 1} / {await event_paginator.get_page_count()}',
                callback_data=PaginationCallback(
                    object_name='EVENT',
                ).pack(),
            ),
            InlineKeyboardButton(
                text=Pagination.NEXT if next_page is not None else ' ',
                callback_data=PaginationCallback(
                    object_name='EVENT',
                    page=next_page,
                    mode=list_mode.value,
                ).pack(),
            ),
        )

    return builder.as_markup()


def get_keyboard_for_link(
        url: str,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для получения ссылки на календарь"""
    builder = InlineKeyboardBuilder()

    url_button = get_url_button(url, EventButton.ADD_IN_CALENDAR)
    builder.add(url_button)
    return builder.as_markup()
