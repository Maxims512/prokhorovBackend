from pydantic import BaseModel, Field, ConfigDict

class PlaneSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    plane_id: int
    airline_id: int
    year_of_release: int
    aircraft_model_id: int