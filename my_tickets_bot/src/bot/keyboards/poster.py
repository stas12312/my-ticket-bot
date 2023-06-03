from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asyncpg import Record

from bot.buttons import Action
from bot.callbacks import PaginationCallback
from bot.keyboards.utils import CLOSE_BUTTON, get_pagination_buttons
from bot.paginators import PosterPaginator


def get_location_for_poster(
        locations: list[Record],
) -> types.InlineKeyboardMarkup:
    """Получение клавиатуры для выбора места для отображения афишы"""
    builder = InlineKeyboardBuilder()

    for location in locations:
        builder.row(
            InlineKeyboardButton(
                text=location['name'],
                callback_data=PaginationCallback(
                    object_name='POSTER',
                    page=0,
                    mode=location['parser_id'],
                ).pack(),
            )
        )

    builder.row(
        CLOSE_BUTTON,
    )

    return builder.as_markup()


async def get_for_poster_events(
        poster_paginator: PosterPaginator,
) -> types.InlineKeyboardMarkup:
    """Формирование клавиатуры с пагинацией"""
    builder = InlineKeyboardBuilder()

    if await poster_paginator.get_page_count() > 1:
        buttons = await get_pagination_buttons(poster_paginator.parser_id, poster_paginator, 'POSTER')
        builder.row(*buttons)

    builder.row(
        InlineKeyboardButton(
            text=Action.BACK,
            callback_data=PaginationCallback(
                object_name='POSTER',
                page=0,
                mode=0,
            ).pack(),
        ),
    )
    builder.row(
        CLOSE_BUTTON,
    )

    return builder.as_markup()
