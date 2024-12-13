from pydantic import BaseModel, ConfigDict


class AirlineCreateUpdateSchema(BaseModel):
    title: str
    rating: float


class AirlineSchema(AirlineCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    airline_id: int
