from pydantic import BaseModel, ConfigDict

class DiscountSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    discount_id: int
    customer_id: int
    discount_percent: int
