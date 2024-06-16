from fastapi.routing import APIRouter
from .weather.router import router as weather_router


def get_routes() -> list[APIRouter]:
    return [
        weather_router,
    ]
