from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot.callbacks import CityCallback, EntityAction
from bot.forms import LocationForm, CityForm
from bot.messages import quote
from bot.services.cities.messages import make_city_message
from services.city import get_timezone_name
from services.repositories import Repo


async def processing_name_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repo,
):
    """
    Обработка введенного названия города,
    для дальнейшей корректной работы требуется наличие названия часового пояса
    который будет получен по названию города
    """
    name = message.text
    if (timezone_name := await get_timezone_name(name)) is None:
        await message.answer(f'Не удалось найти город "{quote(name)}", попробуйте еще раз')
        return

    await state.clear()

    city = await repo.city.get_by_name(message.from_user.id, name, True)
    if not city:
        added_city = await repo.city.create(message.from_user.id, name, timezone_name)
        await message.answer(f'✅ Город добавлен ✅ \n\n{make_city_message(added_city)}')
        # Запускаем диалог добавления места
        await message.answer('Введите название места проведения мероприятий')
        await state.set_state(LocationForm.input_name)
        await state.update_data(city_id=added_city.city_id)
    elif city.is_deleted:
        await repo.city.restore(message.from_user.id, city.city_id)
        await message.answer('✅ Город был восстановлен ✅')
    else:
        await message.answer('⚠️ Данный город уже добавлен ⚠️')


async def start_add_city_handler(
        query: types.CallbackQuery,
        state: FSMContext,
):
    """Начало процесса добавления города"""
    await state.set_state(CityForm.name)
    await query.message.delete()
    await query.message.answer('Введите название города')


router = Router()
router.callback_query.register(start_add_city_handler, CityCallback.filter(F.action == EntityAction.ADD))
router.message.register(processing_name_handler, CityForm.name)
