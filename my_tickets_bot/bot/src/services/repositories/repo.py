"""Основной репозиторй"""
from asyncpg import Connection

from .city import CityRepo
from .common import CommonRepo
from .event import EventRepo
from .file import FileRepo
from .location import LocationRepo
from .parser import ParserRepo
from .ticket import TicketRepo
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
        self.common = CommonRepo(connection)
        self.parser = ParserRepo(connection)
