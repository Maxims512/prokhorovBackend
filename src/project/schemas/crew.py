from pydantic import BaseModel, ConfigDict


class CrewCreateUpdateSchema(BaseModel):
    pilot1_id: int
    pilot2_id: int
    stewardess_id: int


class CrewSchema(CrewCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    crew_id: int
