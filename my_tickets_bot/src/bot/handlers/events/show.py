"""Отображение мероприятия"""
import datetime

from aiogram import Router, F
from aiogram import types
from aiogram.filters import Text

from bot.buttons import MainMenu
from bot.callbacks import EventCallback, EntityAction
from bot.keybaords import get_actions_for_event, get_actions_for_edit_event
from bot.messages import make_event_message
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
    actual_time = datetime.datetime.now() - datetime.timedelta(hours=12)
    events = await repo.event.list(message.from_user.id, is_actual=True, actual_time=actual_time)

    events_message = [make_event_message(ticket, with_command=True) for ticket in events]

    msg = '\n\n'.join(events_message) or 'У вас нет мероприятий'

    await message.answer(msg, disable_web_page_preview=True)


async def event_card_handler(
        message: types.Message,
        repo: Repo,
):
    """Получение карточки билета"""
    event_id = int(message.text.split('_')[1])
    event = await repo.event.get(message.from_user.id, event_id)
    tickets = await repo.ticket.list_for_event(message.from_user.id, event.event_id)

    event_message = make_event_message(event)
    keyboards = get_actions_for_event(event, tickets)

    await message.answer(
        text=event_message,
        reply_markup=keyboards,
        disable_web_page_preview=True,
    )


router = Router()
router.message.register(my_events_handler, Text(text=MainMenu.MY_EVENTS))

router.message.register(event_card_handler, Text(startswith='/event_'))
router.callback_query.register(show_edits_handler, EventCallback.filter(F.action == EntityAction.EDIT))
router.callback_query.register(show_event_handler, EventCallback.filter(F.action == EntityAction.SHOW))
