"""Добавление мероприятия"""
import validators
from aiogram import types, Router, F
from aiogram.filters import or_f, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

from bot.buttons import Action, MainMenu
from bot.forms import EventForm
from bot.keyboards.city import get_add_city_keyboard
from bot.keyboards.common import get_menu_keyboard
from bot.keyboards.utils import get_keyboard_by_values
from bot.messages.location import get_address
from bot.messages.templates import TIME_EXAMPLES
from bot.utils import save_ticket
from services.event_time import parse_datetime, get_localtime
from services.repositories import Repo


async def start_add_event_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Добавление события"""
    cities = await repo.city.list(message.from_user.id)

    keyboard = get_keyboard_by_values([city.name for city in cities])

    if not cities:
        await message.answer(
            text='Для добавления события необходимо добавить город и место',
            reply_markup=get_add_city_keyboard(),
        )
        return

    # Если требуется выбрать город, то выводим список
    if len(cities) >= 2:
        await message.answer('Выберите город', reply_markup=keyboard)
        await state.set_state(EventForm.city_id)
        return

    city = cities[0]
    await state.update_data(city_id=city.city_id)

    locations = await repo.location.list(message.from_user.id, city.city_id)

    # Если необходимо выбрать локацию
    keyboard = get_keyboard_by_values([location.name for location in locations])
    if len(locations) >= 2:
        await message.answer(f'🏙️ {city.name}')
        await message.answer('Выберите место проведения', reply_markup=keyboard)
        await state.set_state(EventForm.location_id)
        return

    # Переходим на этап ввода названия, так как город и локация в единственном экземпляре
    location = locations[0]
    await state.update_data(location_id=location.location_id)
    await state.set_state(EventForm.event_name)
    await message.answer(f'🏙️ {city.name}\n🏛️ {location.name}\n📍 {get_address(location)}')
    await message.answer('Введите название мероприятия', reply_markup=types.ReplyKeyboardRemove())


async def processing_city_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка места"""
    city_name = message.text

    if (city := await repo.city.get_by_name(message.from_user.id, city_name)) is None:
        await message.answer('Не удалось определить город, повторите попытку')
        return

    places = await repo.location.list(message.from_user.id, city.city_id)
    keyboard = get_keyboard_by_values([place.name for place in places])

    await message.answer('Выберите место проведения', reply_markup=keyboard)

    await state.update_data(city_id=city.city_id)
    await state.set_state(EventForm.location_id)


async def processing_place_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка выбранного место"""
    location_name = message.text

    if (location := await repo.location.get_by_name(message.from_user.id, location_name)) is None:
        await message.answer('Не удалось определить место, повторите попытку')
        return

    await message.answer('Введите название мероприятия', reply_markup=types.ReplyKeyboardRemove())

    await state.update_data(location_id=location.location_id)
    await state.set_state(EventForm.event_name)


async def processing_name_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введенного названия"""
    await message.answer(f'Введите дату и время проведения мероприятия\n{TIME_EXAMPLES}')
    await state.update_data(event_name=message.text)
    await state.set_state(EventForm.event_time)


async def processing_event_time_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка введенной даты"""
    raw_datetime = message.text

    data = await state.get_data()
    city_id = data.get('city_id')
    city = await repo.city.get(message.from_user.id, city_id)

    now = get_localtime(city.timezone)

    if (parsed_datetime := parse_datetime(raw_datetime, city.timezone, now)) is None:
        await message.answer('Не удалось определить дату и время, попробуйте еще раз')
        return

    keyboard = get_keyboard_by_values([Action.PASS])
    await message.answer('Отправьте ссылку на мероприятие', reply_markup=keyboard)

    await state.update_data(event_time=parsed_datetime)
    await state.set_state(EventForm.event_link)


async def processing_link_handler(
        message: types.Message,
        state: FSMContext,
):
    """Обработка введения ссылки на мероприятие"""
    is_pass = message.text == Action.PASS

    if not validators.url(message.text) and not is_pass:
        await message.answer('Некорректная ссылка, попробуйте еще раз')
        return

    if not is_pass:
        await state.update_data(event_link=message.text)
    keyboard = get_keyboard_by_values([Action.PASS])
    await message.answer(
        text='Отправьте билет',
        reply_markup=keyboard,
    )
    await state.set_state(EventForm.file_id)


async def processing_file(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """Обработка файла"""
    is_pass = message.text == Action.PASS

    data = await state.get_data()

    event = await repo.event.save(
        user_id=message.from_user.id,
        location_id=data['location_id'],
        name=data['event_name'],
        event_time=data['event_time'],
        link=data.get('event_link'),
    )

    if not is_pass:
        await save_ticket(
            event_id=event.event_id,
            message=message,
            repo=repo,
        )

    await message.answer('Событие добавлено', reply_markup=get_menu_keyboard())
    await state.clear()


router = Router()
router.message.register(start_add_event_handler, Text(text=MainMenu.ADD_EVENT))
router.message.register(processing_city_handler, EventForm.city_id)
router.message.register(processing_place_handler, EventForm.location_id)
router.message.register(processing_name_handler, EventForm.event_name)
router.message.register(processing_event_time_handler, EventForm.event_time)
router.message.register(processing_link_handler, EventForm.event_link)
router.message.register(
    processing_file,
    or_f(EventForm.file_id, F.content_type.in_([ContentType.DOCUMENT, ContentType.PHOTO])),
    or_f(EventForm.file_id, Text(text=Action.PASS)),
)
