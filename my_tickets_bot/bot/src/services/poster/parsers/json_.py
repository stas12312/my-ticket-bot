import abc
import json

from .web import WebParser, RequestData


class JsonParser(WebParser, abc.ABC):
    """Стратегия для JSON"""

    async def _get_prepared_data_from_url(
            self,
            request_data: RequestData,
    ) -> dict:
        body = await self.get_data_from_url(
            url=request_data.url,
            params=request_data.params,
            headers={
                'X-Requested-With': 'XMLHttpRequest',
            },
        )
        return json.loads(body)
