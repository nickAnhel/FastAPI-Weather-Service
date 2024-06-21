from fastapi.routing import APIRouter
from .weather.router import router as weather_router
from .auth.router import auth_router, user_router


def get_routes() -> list[APIRouter]:
    return [
        weather_router,
        auth_router,
        user_router,
    ]
