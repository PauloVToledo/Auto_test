from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))  # Relación con el auto
    customer_phone = Column(String)
    customer_email = Column(String)
    customer_name = Column(String)
    date = Column(DateTime)

    # Opcional: Esto permite acceder a los datos del auto desde la cita (ej: cita.vehicle.brand)
    vehicle = relationship("Vehicle")
