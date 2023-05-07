from .alexandrinsky import AlexandrinskySpb
from .big_dramatic_theatre import BigDramaticTheaterSpb
from .malyshchitsky import MalyshchitskyParserSpb

parsers = [
    MalyshchitskyParserSpb(),
    BigDramaticTheaterSpb(),
    AlexandrinskySpb(),
]
