from pydantic import BaseModel, ConfigDict

class CrewSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crew_id: int
    pilot1_id: int  # Reference to 'Staff.employee_id'
    pilot2_id: int  # Reference to 'Staff.employee_id'
    stewardess_id: int  # Reference to 'Staff.employee_id'
