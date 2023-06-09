from services.poster.parsers import WebParser
from . import nsk
from . import spb

PARSERS: list[WebParser] = [
    *nsk.parsers,
    *spb.parsers,
]
