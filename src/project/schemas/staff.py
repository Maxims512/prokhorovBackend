from pydantic import BaseModel, ConfigDict
class StaffSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employee_id: int
    first_name: str
    last_name: str
    airline_id: int
    experience: int
