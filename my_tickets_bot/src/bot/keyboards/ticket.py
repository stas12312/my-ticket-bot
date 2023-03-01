from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons import Action
from bot.callbacks import TicketCallback, EntityAction
from bot.keyboards.utils import CLOSE_BUTTON
from models import Ticket


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
