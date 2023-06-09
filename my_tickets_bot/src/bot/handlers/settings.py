"""Обработчики для настроек"""
from aiogram import Router, F
from aiogram import types
from aiogram.filters import Text

from ..buttons import MainMenu
from ..callbacks import SettingsCallback, EntityAction
from ..keyboards.setting import get_settings_menu


async def my_settings_handler(
        message_or_query: types.Message | types.CallbackQuery,
):
    """Отображение настроек"""
    text = '⚙ _Настройки_\n\n' \
           'ℹ️ Выберите нужный пункт'
    keyboard = get_settings_menu()
    if isinstance(message_or_query, types.Message):
        await message_or_query.answer(text, reply_markup=keyboard)
        await message_or_query.delete()
    else:
        await message_or_query.message.edit_text(text, reply_markup=keyboard)


settings_router = Router()
settings_router.message.register(my_settings_handler, Text(text=MainMenu.SETTINGS))
settings_router.callback_query.register(my_settings_handler, SettingsCallback.filter(F.action == EntityAction.SHOW))
