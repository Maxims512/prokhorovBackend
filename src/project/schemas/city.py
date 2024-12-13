from pydantic import BaseModel, ConfigDict


class CityCreateUpdateSchema(BaseModel):
    title: str
    country: str


class CitySchema(CityCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    city_id: int
