from pydantic import BaseModel, ConfigDict


class RouteCreateUpdateSchema(BaseModel):
    departure_airport_id: int
    arrival_airport_id: int
    distance: float


class RouteSchema(RouteCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    route_id: int
