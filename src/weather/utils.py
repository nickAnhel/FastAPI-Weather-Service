from aiohttp import ClientSession

from ..config import settings


async def get_weather(city: str):
    async with ClientSession() as session:
        params = {"q": city, "APPID": settings.weather_api_key}
        async with session.get(url=settings.weather_api_url, params=params) as response:  # type: ignore
            return await response.json()
