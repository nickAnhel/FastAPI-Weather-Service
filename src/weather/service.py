from .utils import get_weather
from .scemas import WeatherSchema, TemperatureSchema, WindSchema, CloudsSchema
from .exceptions import WeatherNotFound


class WeatherService:
    async def get_weather_by_city(self, *, city: str) -> WeatherSchema:
        try:
            weather = await get_weather(city)
            return WeatherSchema(
                city=city,
                main=weather["weather"][0]["main"],
                description=weather["weather"][0]["description"],
                temperature=TemperatureSchema(
                    value=round(weather["main"]["temp"] - 273.15, 2),
                    feels_like=round(weather["main"]["feels_like"] - 273.15, 2),
                    min=round(weather["main"]["temp_min"] - 273.15, 2),
                    max=round(weather["main"]["temp_max"] - 273.15, 2),
                ),
                pressure=weather["main"]["pressure"],
                humidity=weather["main"]["humidity"],
                wind=WindSchema(
                    speed=weather["wind"]["speed"],
                    deg=weather["wind"]["deg"],
                ),
                clouds=CloudsSchema(
                    all=weather["clouds"]["all"],
                ),
            )
        except KeyError as exc:
            raise WeatherNotFound(city=city) from exc


weather_service = WeatherService()
