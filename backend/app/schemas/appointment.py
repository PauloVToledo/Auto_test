from pydantic import BaseModel, field_validator
from datetime import datetime


# Esto valida los datos que llegan del Frontend
class AppointmentCreate(BaseModel):
    vehicle_id: int
    customer_name: str
    customer_email: str
    customer_phone: str
    date: datetime

    # --- VALIDACIÓN DE HORARIO ---
    @field_validator("date")
    def check_business_hours(cls, v):
        # v es el objeto datetime
        # v.hour devuelve la hora en formato 24h (0-23)

        # Regla: Debe ser mayor o igual a 9 Y menor estricto a 18
        # (Esto permite citas hasta las 17:59, pero rechaza las 18:00 en adelante)
        if v.hour < 9 or v.hour >= 18:
            raise ValueError("Nuestras sucursales solo atienden de 09:00 a 18:00 hrs.")

        return v
