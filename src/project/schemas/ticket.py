from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TicketCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    date_of_purchase: datetime
    price: float
    flight_id: int


class TicketSchema(TicketCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: int
