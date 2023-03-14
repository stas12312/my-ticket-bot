from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons import Action, Event as EventButton, Settings, Pagination
from bot.callbacks import TicketCallback, EntityAction, EventCallback, EditEventCallback, EditEventField, \
    PaginationCallback
from bot.keyboards.utils import CLOSE_BUTTON
from bot.paginator import EventPaginator
from models import Event, Ticket
from .common import get_url_button


def get_actions_for_event(
        event: Event,
        tickets: list[Ticket],
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

    builder.row(
        InlineKeyboardButton(
            text=Action.DELETE,
            callback_data=EventCallback(action=EntityAction.DELETE, event_id=event.event_id).pack(),
        ),
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
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для списка мероприятий"""
    builder = InlineKeyboardBuilder()

    prev_page = event_paginator.prev_page() if await event_paginator.has_prev() else None
    next_page = event_paginator.next_page() if await event_paginator.has_next() else None

    builder.row(
        InlineKeyboardButton(
            text=Pagination.PREV if prev_page is not None else ' ',
            callback_data=PaginationCallback(
                object_name='EVENT',
                page=prev_page,
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
            ).pack(),
        ),
    )

    return builder.as_markup()


def get_keyboard_for_link(
        url: str,
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для получения ссылки на календарь"""
    builder = InlineKeyboardBuilder()

    url_button = get_url_button(url, '🗓 Добавить в календарь')
    builder.add(url_button)
    return builder.as_markup()
