from asyncpg import Connection

from .city import CityRepo
from .event import EventRepo
from .file import FileRepo
from .ticket import TicketRepo
from .location import LocationRepo
from .user import UserRepo


class Repo:
    """Репозиторий для всех сущностей"""

    def __init__(
            self,
            connection: Connection,
    ):
        self.user = UserRepo(connection)
        self.city = CityRepo(connection)
        self.location = LocationRepo(connection)
        self.file = FileRepo(connection)
        self.ticket = TicketRepo(connection)
        self.event = EventRepo(connection)
