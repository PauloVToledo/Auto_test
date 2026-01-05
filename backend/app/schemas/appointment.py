from pydantic import BaseModel
from datetime import datetime


# Esto valida los datos que llegan del Frontend
class AppointmentCreate(BaseModel):
    vehicle_id: int
    customer_phone: str
    date: datetime
