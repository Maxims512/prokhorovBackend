from pydantic import BaseModel, ConfigDict


class DiscountCreateUpdateSchema(BaseModel):
    customer_id: int
    discount_percent: int


class DiscountSchema(DiscountCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    discount_id: int
