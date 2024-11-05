from pydantic import BaseModel, Field, ConfigDict


class CustomerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    age: int