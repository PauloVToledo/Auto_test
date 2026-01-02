from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate
from app.services import booking_service, whatsapp_service
from app.core.database import get_db

router = APIRouter()


@router.post("/")
def create_appointment(
    booking_data: AppointmentCreate,
    background_tasks: BackgroundTasks,  # Para no trabar la respuesta
    db: Session = Depends(get_db),
):
    # 1. Intentar crear la reserva en la BD
    try:
        new_booking = booking_service.create_booking(db, booking_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Enviar notificaciones (En segundo plano para que la web responda rápido)
    # Notificar al Vendedor
    background_tasks.add_task(
        whatsapp_service.send_message,
        to=new_booking.seller.phone,
        body=f"Nueva cita agendada para {new_booking.vehicle.name} a las {new_booking.date}",
    )

    # Notificar al Comprador
    background_tasks.add_task(
        whatsapp_service.send_message,
        to=new_booking.customer_phone,
        body=f"Hola! Tu visita para el {new_booking.vehicle.name} quedó confirmada.",
    )

    return {"status": "ok", "booking_id": new_booking.id}
