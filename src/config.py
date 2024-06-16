from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    DESCRIPTION: str

    WEATHER_API_URL: str | None = None
    WEATHER_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings(
    PROJECT_NAME="Weather API",
    VERSION="0.1.0",
    DEBUG=True,
    DESCRIPTION="API for Weather Service",
)
