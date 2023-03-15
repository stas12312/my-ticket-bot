"""Роутер с общими обработчиками"""
import datetime

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from services.event_time import parse_date
from services.repositories import Repo
from services.statistic import get_user_statistic
from ..callbacks import CloseCallback
from ..commands import AppCommand as MyCommand
from ..forms import CityForm, CheckDateForm
from ..keyboards.common import get_menu_keyboard
from ..messages.event import make_event_message
from ..messages.statistic import get_message_for_statistic
from ..messages.templates import DATE_EXAMPLES
from ..messages.utils import quote


async def start_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработчик команды /start"""

    user = message.from_user
    user_has_cities = await repo.city.user_has_cities(user.id, with_deleted=True)

    await repo.user.save(user.id, user.username, user.first_name, user.last_name)

    keyboard = get_menu_keyboard() if user_has_cities else None

    await message.answer(
        text='Приветствуем в "Мои билеты"',
        reply_markup=keyboard,
    )
    # Если у пользователя нет городов, предлагаем его добавить
    if not user_has_cities:
        await message.answer('Для начала работы необходимо добавить город\nВведите название города')
        await state.set_state(CityForm.name)


async def close_menu(
        query: types.CallbackQuery,
):
    """Закрытие меню"""
    await query.message.delete()


async def cancel(
        message: types.Message,
        state: FSMContext,
):
    """Отмена текущего действия"""
    await state.clear()
    await message.answer('Действие отменено', reply_markup=get_menu_keyboard())


async def statistic(
        message: types.Message,
        repo: Repo,
):
    """Отображение статистики"""
    now = datetime.datetime.utcnow()
    rows = await get_user_statistic(message.from_user.id, now, repo)
    msg = get_message_for_statistic(rows)
    await message.answer(msg)


async def check_date(
        message: types.Message,
        state: FSMContext,
):
    """Проверка мероприятий на переданную дату"""
    await message.answer(f'Введите дату, для которой необходимо проверить наличие мероприятий\n'
                         f'{DATE_EXAMPLES}')
    await state.set_state(CheckDateForm.input_date)


async def show_events_on_date(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Отображение мероприятий на введенную дату"""
    now = datetime.datetime.utcnow()
    date = parse_date(message.text, now)
    if not date:
        await message.answer('Не удалось определить дату, попробуйте еще раз')
        return

    event_ids_for_date = await repo.common.get_event_ids_for_date(message.from_user.id, date)
    if not event_ids_for_date:
        await message.answer('На данную дату мероприятий не найдено')
        return

    events = await repo.event.list(message.from_user.id, event_ids=event_ids_for_date)

    title = f'Ваши события на {message.text}'
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
    msg = '\n\n'.join(events_message)
    await message.answer(f'{quote(title)}\n\n{msg}', disable_web_page_preview=True)
    await state.clear()


common_handlers = Router()

common_handlers.message.register(start_handler, Command(commands=MyCommand.START))
common_handlers.callback_query.register(close_menu, CloseCallback.filter())
common_handlers.message.register(cancel, Command(commands=MyCommand.CANCEL))
common_handlers.message.register(statistic, Command(commands=MyCommand.STATISTIC))
common_handlers.message.register(check_date, Command(commands=MyCommand.CHECK_DATE))
common_handlers.message.register(show_events_on_date, CheckDateForm.input_date)
