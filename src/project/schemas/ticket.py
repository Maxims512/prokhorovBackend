from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TicketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: int
    customer_id: int
    date_of_purchase: datetime
    price: float
    flight_id: int