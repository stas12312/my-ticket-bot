from asyncpg import Connection

from services.repositories.city import CityRepo
from services.repositories.place import PlaceRepo
from services.repositories.user import UserRepo


class Repo:
    """Репозиторий для всех сущностей"""

    def __init__(
            self,
            connection: Connection,
    ):
        self.user = UserRepo(connection)
        self.city = CityRepo(connection)
        self.place = PlaceRepo(connection)
