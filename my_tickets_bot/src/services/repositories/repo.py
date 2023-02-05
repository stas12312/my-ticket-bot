from asyncpg import Connection

from .city import CityRepo
from .place import PlaceRepo
from .ticket import TicketRepo
from .user import UserRepo
from .file import FileRepo


class Repo:
    """Репозиторий для всех сущностей"""

    def __init__(
            self,
            connection: Connection,
    ):
        self.user = UserRepo(connection)
        self.city = CityRepo(connection)
        self.place = PlaceRepo(connection)
        self.ticket = TicketRepo(connection)
        self.file = FileRepo(connection)
