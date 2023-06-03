from aiogram import Router, F
from aiogram import types
from aiogram.filters import Text

from bot.buttons import MainMenu
from bot.callbacks import PaginationCallback
from bot.keyboards.poster import get_location_for_poster, get_for_poster_events
from bot.messages.poster import make_poster_event_message
from bot.paginators import PosterPaginator
from services.repositories import Repo


async def show_available_location(
        message_or_query: types.Message | types.CallbackQuery,
        repo: Repo,
):
    """Отображение списка доступных для получения афишы локаций"""
    locations = await repo.parser.get_supported_locations(message_or_query.from_user.id)
    if not locations:
        await message_or_query.answer('Нет доступных мест')
        return

    keyboard = get_location_for_poster(locations)
    if isinstance(message_or_query, types.Message):
        await message_or_query.answer(
            text='Выберите место для просмотра афишы',
            reply_markup=keyboard,
        )
    else:
        await message_or_query.message.edit_text(
            text='Выберите место для просмотра афишы',
            reply_markup=keyboard,
        )


async def show_poster(
        query: types.CallbackQuery,
        callback_data: PaginationCallback,
        repo: Repo,
):
    """Отображение афишы"""
    parser_id = callback_data.mode
    page = callback_data.page
    paginator = PosterPaginator(page, 6, repo, parser_id)
    keyboard = await get_for_poster_events(paginator)
    events = await paginator.get_data()

    message = '\n'.join([make_poster_event_message(e) for e in events]) if events else 'Мероприятия отсутствуют'

    await query.message.edit_text(
        text=message,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


router = Router()
router.message.register(show_available_location, Text(text=MainMenu.POSTER))
router.callback_query.register(
    show_available_location,
    PaginationCallback.filter((F.object_name == 'POSTER') & (F.mode == 0))
)
router.callback_query.register(show_poster, PaginationCallback.filter(F.object_name == 'POSTER'))
