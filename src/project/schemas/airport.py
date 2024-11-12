from pydantic import BaseModel, ConfigDict

class AirportSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    airport_id: int
    city_id: int
    airport_code: str