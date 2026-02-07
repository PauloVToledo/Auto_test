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
    def validate_date_rules(cls, v):
        """
        Validate the business rules for an appointment date.

        Args:
            v (datetime): The appointment date to validate.

        Raises:
            ValueError: If the date falls on a weekend (Saturday or Sunday).
            ValueError: If the appointment time is outside business hours (9:00 AM to 6:00 PM).
            ValueError: If the appointment minute is not on the hour (e.g., 10:15 AM).

        Returns:
            datetime: The validated appointment date.
        """
        # 1. Regla: Lunes (0) a Viernes (4). Sábado(5) y Domingo(6) prohibidos.
        if v.weekday() >= 5:
            raise ValueError("❌ Error: No atendemos fines de semana.")

        # 2. Regla: Horario 09:00 a 18:00
        if v.hour < 9 or v.hour >= 18:
            raise ValueError("❌ Error: Horario de atención es de 09:00 a 18:00.")

        # 3. Regla: Minutos en 00 (Opcional, para evitar citas a las 9:15 si usas slots fijos)
        if v.minute != 0:
            raise ValueError(
                "❌ Error: Las citas son por hora en punto (ej: 10:00, 11:00)."
            )

        return v
