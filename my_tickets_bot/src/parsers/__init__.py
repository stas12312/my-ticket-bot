from .nsk import (
    OldHouseParser,
    RedTorchParser,
    GlobusParser,
)

PARSERS = [
    OldHouseParser(),
    RedTorchParser(),
    GlobusParser(),
]
