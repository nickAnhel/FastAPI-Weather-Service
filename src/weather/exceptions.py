class WeatherNotFound(Exception):
    def __init__(self, city: str) -> None:
        super().__init__(f"Weather for city {city} not found")
