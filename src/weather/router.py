from fastapi import APIRouter, HTTPException

from .scemas import WeatherSchema
from .service import weather_service
from .exceptions import WeatherNotFound


router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)


@router.get("/")
async def get_weather(city: str) -> WeatherSchema:
    try:
        return await weather_service.get_weather_by_city(city=city)
    except WeatherNotFound as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong",
        ) from exc
