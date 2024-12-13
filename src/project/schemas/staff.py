from pydantic import BaseModel, ConfigDict


class StaffCreateUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    airline_id: int
    experience: int


class StaffSchema(StaffCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    employee_id: int
