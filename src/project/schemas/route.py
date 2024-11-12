from pydantic import BaseModel, ConfigDict
from datetime import time
class RouteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    route_id: int
    departure_airport_id: int
    arrival_airport_id: int
    distance: float
    flight_time: time
