"""Middleware для создания подключения и сессии к бд"""
import logging
from collections.abc import Callable, Awaitable
from typing import Any

from aiogram.types import Update

from services.config import Config

logger = logging.getLogger(__name__)


class ConfigMiddleware:
    """Создание подключения и сессии"""

    def __init__(
            self,
            config: Config,
    ):
        self.config = config

    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ) -> Any:
        """
        Вызов обработчика
        Перед каждым обработчиком создаем соединение и сессию с БД,
        затем пробрасываем его в репозиторий
        """
        data['config'] = self.config
        return await handler(event, data)
