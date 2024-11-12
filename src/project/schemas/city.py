from pydantic import BaseModel, ConfigDict

class CitySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city_id: int
    title: str
    country: str