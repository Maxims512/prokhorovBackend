from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FlightCreateUpdateSchema(BaseModel):
    route_id: int
    plane_id: int
    crew_id: int
    airline_id: int
    departure_time: datetime
    arrival_time: datetime


class FlightSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    flight_id: int
