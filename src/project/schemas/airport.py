from pydantic import BaseModel, ConfigDict


class AirportCreateUpdateSchema(BaseModel):
    city_id: int
    airport_code: str


class AirportSchema(AirportCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    airport_id: int
