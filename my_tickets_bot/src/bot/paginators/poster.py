from services.paginator import BasePaginator
from services.repositories import Repo


class PosterPaginator(BasePaginator):
    """Пагинация для афишы"""

    def __init__(
            self,
            number: int,
            size: int,
            repo: Repo,
            parser_id: int,
    ):
        super().__init__(
            number=number,
            size=size,
        )
        self.repo = repo
        self.parser_id = parser_id

    async def get_total(self) -> int:
        return await self.repo.parser.get_parser_events_count(self.parser_id)

    async def get_data(self) -> list:
        return await self.repo.parser.get_parser_events(
            parser_id=self.parser_id,
            limit=self.size,
            offset=self.get_offset(),
        )
