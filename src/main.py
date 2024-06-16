from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .config import settings
from .routes import get_routes


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
)

for route in get_routes():
    app.include_router(route)


@app.get("/")
async def root():
    return RedirectResponse("/docs")
