from pydantic import BaseModel, ConfigDict


class PlaneCreateUpdateSchema(BaseModel):
    airline_id: int
    year_of_release: int
    aircraft_model_id: int


class PlaneSchema(PlaneCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    plane_id: int
