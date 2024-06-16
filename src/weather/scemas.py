from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TemperatureSchema(BaseSchema):
    value: float
    feels_like: float
    min: float
    max: float


class WindSchema(BaseSchema):
    speed: float
    deg: float


class CloudsSchema(BaseSchema):
    all: int


class WeatherSchema(BaseSchema):
    city: str
    main: str
    description: str
    temperature: TemperatureSchema
    pressure: int
    humidity: int
    wind: WindSchema
    clouds: CloudsSchema
