from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .config import settings
from .routes import get_routes
from .database import create_tables, drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    await create_tables()
    yield


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    lifespan=lifespan,
)

for route in get_routes():
    app.include_router(route)


@app.get("/")
async def root():
    return RedirectResponse("/docs")
