from collections.abc import Callable, Awaitable
from typing import Any

from aiogram.types import Update

from services.config import Config
from services.object_storage import create_session
from aiobotocore.config import AioConfig

class S3Middleware():
    """Создание подключения и сессии для S3"""

    def __init__(
            self,
            config: Config
    ):
        self._config = config
        self._s3_session = create_session(config)

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
        async with self._s3_session.client(
                's3',
                endpoint_url=self._config.s3_endpoint_url,
                config=AioConfig(s3={'addressing_style': 'path'}),
        ) as s3_client:
            data['s3_client'] = s3_client
            data['config'] = self._config
            return await handler(event, data)
