from .globus import GlobusParser
from .old_house import OldHouseParser
from .podzemka import PodzemkaNskParser
from .red_torch import RedTorchParser

parsers = (
    GlobusParser(),
    RedTorchParser(),
    OldHouseParser(),
    PodzemkaNskParser(),
)
