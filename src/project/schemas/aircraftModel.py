from pydantic import BaseModel, ConfigDict
class AircraftModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    aircraft_model_id: int
    title: str
    capacity: int
    max_range: int