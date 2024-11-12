from pydantic import BaseModel, ConfigDict
class AirlineSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    airline_id: int
    title: str
    rating: float