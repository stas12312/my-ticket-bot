"""Работа с городами"""
from dataclasses import dataclass

import aiohttp
from tzfpy import get_tz

QUERY_TEMPLATE = 'https://nominatim.openstreetmap.org/search?q={name}&format=json'


@dataclass
class Coordinate:
    """Координаты"""
    lat: float
    lon: float


def make_query_url(name: str) -> str:
    """Формирование строки запроса"""
    return QUERY_TEMPLATE.format(name=name)


async def get_coordinate(
        name: str
) -> Coordinate | None:
    """Получение координат города по названию"""

    url = make_query_url(name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            cities = await response.json()

    if not cities:
        return None

    city = cities[0]

    return Coordinate(float(city['lat']), float(city['lon']))


async def get_timezone_name(
        name: str,
) -> str | None:
    """Определение названия временной зоны по названию города"""
    coordinate = await get_coordinate(name)
    if not coordinate:
        return None

    return get_tz(coordinate.lon, coordinate.lat)
