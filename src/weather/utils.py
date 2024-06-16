from aiohttp import ClientSession

from ..config import settings


async def get_weather(city: str):
    async with ClientSession() as session:
        params = {"q": city, "APPID": settings.WEATHER_API_KEY}
        async with session.get(url=settings.WEATHER_API_URL, params=params) as response:  # type: ignore
            return await response.json()
