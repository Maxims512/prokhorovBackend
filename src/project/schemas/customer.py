from pydantic import BaseModel, ConfigDict, Field


class CustomerCreateUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str = Field(pattern=r"^\S+@\S+\.\S+$", examples=["email@mail.ru"])
    password: str
    is_admin: bool = False


class CustomerSchema(CustomerCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
