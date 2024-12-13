from pydantic import BaseModel, ConfigDict


class AircraftModelCreateUpdateSchema(BaseModel):
    title: str
    capacity: int
    max_range: int


class AircraftModelSchema(AircraftModelCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    aircraft_model_id: int
