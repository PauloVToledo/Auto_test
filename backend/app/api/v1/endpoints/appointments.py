from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate
from app.services import booking_service, whatsapp_service
from app.core.database import get_db

from app.models.appointment import Appointment

router = APIRouter()


@router.post("/")
def create_appointment(booking: AppointmentCreate, db: Session = Depends(get_db)):
    # 1. IMPRIMIR POR CONSOLA (Lo que pediste)
    print("\n" + "=" * 40)
    print(f"🔔 NUEVA SOLICITUD DE CITA RECIBIDA")
    print(f"🚗 ID Auto: {booking.vehicle_id}")
    print(f"📱 WhatsApp: {booking.customer_phone}")
    print(f"📅 Fecha: {booking.date}")
    print("=" * 40 + "\n")

    # 2. GUARDAR EN BASE DE DATOS
    try:
        new_appointment = Appointment(
            vehicle_id=booking.vehicle_id,
            customer_phone=booking.customer_phone,
            date=booking.date,
        )

        db.add(new_appointment)
        db.commit()  # Confirma los cambios
        db.refresh(new_appointment)  # Recarga el objeto con el ID generado

        return {
            "status": "success",
            "id": new_appointment.id,
            "msg": "Cita guardada correctamente",
        }

    except Exception as e:
        db.rollback()  # Si falla, deshacer cambios
        print(f"❌ Error al guardar en BD: {e}")
        raise HTTPException(status_code=500, detail="Error guardando la cita")
