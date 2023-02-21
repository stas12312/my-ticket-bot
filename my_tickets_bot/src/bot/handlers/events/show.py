"""Отображение мероприятия"""
import datetime

from aiogram import Router, F
from aiogram import types
from aiogram.filters import Text

from bot.buttons import MainMenu
from bot.callbacks import EventCallback, EntityAction, PaginationCallback
from bot.keybaords import (
    get_actions_for_event,
    get_actions_for_edit_event,
    get_event_list_keyboard,
)
from bot.messages import make_event_message
from bot.paginator import EventPaginator
from services.profile import duration
from services.repositories import Repo


async def show_edits_handler(
        query: types.CallbackQuery,
        callback_data: EventCallback,
):
    """Отображению меню настроек"""
    event_id = callback_data.event_id
    keyboard = get_actions_for_edit_event(event_id)
    await query.message.edit_reply_markup(reply_markup=keyboard)


async def show_event_handler(
        query: types.CallbackQuery,
        callback_data: EventCallback,
        repo: Repo,
):
    """Отображение события"""
    event_id = callback_data.event_id
    event = await repo.event.get(query.from_user.id, event_id)
    tickets = await repo.ticket.list_for_event(query.from_user.id, event_id)
    keyboard = get_actions_for_event(event, tickets)
    event_message = make_event_message(event)
    await query.message.edit_text(
        text=event_message,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


async def my_events_handler(
        message: types.Message,
        repo: Repo,
):
    """Отображения событий пользователя"""
    msg, keyboard = await get_message_with_keyboard(message.from_user.id, 0, repo)
    await message.answer(msg, disable_web_page_preview=True, reply_markup=keyboard)


async def my_events_with_page_handler(
        query: types.CallbackQuery,
        callback_data: EventPaginator,
        repo: Repo,
):
    """Обработка переключения страницы"""
    await query.answer()
    if callback_data.page is None:
        return
    msg, keyboard = await get_message_with_keyboard(query.from_user.id, callback_data.page, repo)
    await query.message.edit_text(msg, disable_web_page_preview=True, reply_markup=keyboard)


@duration
async def get_message_with_keyboard(
        user_id: int,
        page: int,
        repo: Repo,
) -> tuple[str, types.InlineKeyboardMarkup]:
    """Получение сообщения и клавиатуры для списка мероприятий"""
    actual_time = datetime.datetime.now() - datetime.timedelta(hours=12)

    event_paginator = EventPaginator(
        repo=repo,
        user_id=user_id,
        is_actual=True,
        actual_datetime=actual_time,
        number=page,
        size=5,
    )

    events = await event_paginator.get_events()
    events_message = [
        make_event_message(
            event=event,
            with_command=True,
            with_address=False,
            with_left_time=False,
        )
        for event
        in events
    ]

    keyboard = await get_event_list_keyboard(event_paginator) if await event_paginator.get_page_count() > 1 else None

    msg = '\n\n'.join(events_message) or 'У вас нет мероприятий'

    return msg, keyboard


async def event_card_handler(
        message: types.Message,
        repo: Repo,
):
    """Получение карточки билета"""
    event_id = int(message.text.split('_')[1])
    event = await repo.event.get(message.from_user.id, event_id)
    if not event:
        await message.answer('⚠️ Мероприятие не найдено ⚠️')
        return

    tickets = await repo.ticket.list_for_event(message.from_user.id, event.event_id)

    event_message = make_event_message(event)
    keyboards = get_actions_for_event(event, tickets)

    await message.answer(
        text=event_message,
        reply_markup=keyboards,
        disable_web_page_preview=True,
    )
    await message.delete()


router = Router()
router.message.register(my_events_handler, Text(text=MainMenu.MY_EVENTS))

router.message.register(event_card_handler, Text(startswith='/event_'))
router.callback_query.register(show_edits_handler, EventCallback.filter(F.action == EntityAction.EDIT))
router.callback_query.register(show_event_handler, EventCallback.filter(F.action == EntityAction.SHOW))
router.callback_query.register(my_events_with_page_handler, PaginationCallback.filter(F.object_name == 'EVENT'))
