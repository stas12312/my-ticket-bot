from datetime import datetime

import pytz
from aiogram import Bot
from aiogram.utils.markdown import link, bold, italic

from bot.emoji import get_clock_emoji
from bot.messages.location import get_address
from bot.utils import get_func_for_file
from models import Event
from services.config import Config
from services.event_time import get_beatify_datetime, get_interval
from services.repositories import Repo
from .utils import quote, make_message_by_rows
from ..keyboards.event import get_actions_for_event


async def send_event_card(
        bot: Bot,
        user_id: int,
        event_id: int,
        repo: Repo,
        config: Config | None = None,
        title: str | None = None,
        with_preview: bool = False,
):
    """Отправка карточки события"""
    event = await repo.event.get(user_id, event_id)
    if not event:
        return

    tickets = await repo.ticket.list_for_event(user_id, event_id)
    calendar_url = get_event_calendar_url(config.host, event.uuid) if config else None
    event_message = make_event_message(event, title)
    keyboard = get_actions_for_event(event, tickets, calendar_url)

    if len(tickets) == 1 and with_preview:
        ticket = tickets[0]
        func = await get_func_for_file(bot, ticket.file)
        await func(
            user_id,
            ticket.file.bot_file_id,
            caption=event_message,
            reply_markup=keyboard,
        )
        return

    await bot.send_message(
        chat_id=user_id,
        text=event_message,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


def make_event_message(
        event: Event,
        title: str | None = None,
        with_command: bool = False,
        with_address: bool = True,
        with_left_time: bool = True,
) -> str:
    """Формирование сообщения для описания билета"""

    event_link = link(event.name, event.link)
    location_url_name = link(event.location.name, event.location.url)
    now = pytz.utc.localize(datetime.now()).astimezone(pytz.timezone(event.location.city.timezone))

    rows = []
    if title:
        rows.append(title)

    rows.extend([
        f'✨ *{event_link}*',
        f'🏛 *{location_url_name}*',
    ])

    if with_address:
        rows.append(f'📍 {get_address(event.location)}')

    rows.append(f'{get_clock_emoji(event.time)} {bold(get_beatify_datetime(event.time))}')

    if (end_time := get_interval(event.time, event.end_time)) and with_left_time:
        rows.append(f'⏱ {quote(end_time)}')

    if (left_time := get_interval(now, event.time)) and with_left_time:
        rows.append(f'⏳ Через {italic(quote(left_time))}')

    if with_command:
        command = quote(f'/event_{event.event_id}')
        rows.append(f'⚙ Управлять {command}')

    return make_message_by_rows(rows)


def make_message_for_calendar(
        event: Event,
) -> str:
    """Формирование сообщения для события в календаре"""
    rows = [
        f'📍 {get_address(event.location)}',
    ]

    if event.link:
        rows.append(f'🔗 {event.link}')

    return make_message_by_rows(rows)


def get_event_calendar_url(
        host: str,
        event_uuid: str,
) -> str:
    """Получение URL-адреса события для добавления в календарь"""

    return f'{host}/events/{event_uuid}/calendar-ics'
