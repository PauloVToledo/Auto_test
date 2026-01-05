from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate
from app.services import booking_service, whatsapp_service
from app.core.database import get_db

from app.models.appointment import Appointment
from app.models.vehicle import Vehicle


router = APIRouter()


@router.post("/")
def create_appointment(
    booking: AppointmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # 1. IMPRIMIR POR CONSOLA (Lo que pediste)
    print("\n" + "=" * 40)
    print(f"🔔 NUEVA SOLICITUD DE CITA RECIBIDA")
    print(f"🚗 ID Auto: {booking.vehicle_id}")
    print(f"📄 Nombre: {booking.customer_name}")
    print(f"📱 WhatsApp: {booking.customer_phone}")
    print(f"📅 Fecha: {booking.date}")
    print("=" * 40 + "\n")

    # 2. GUARDAR EN BASE DE DATOS
    try:
        new_appointment = Appointment(
            vehicle_id=booking.vehicle_id,
            customer_name=booking.customer_name,
            customer_phone=booking.customer_phone,
            date=booking.date,
        )

        db.add(new_appointment)
        db.commit()  # Confirma los cambios
        db.refresh(new_appointment)  # Recarga el objeto con el ID generado.

    except Exception as e:
        db.rollback()  # Si falla, deshacer cambios
        print(f"❌ Error al guardar en BD: {e}")
        raise HTTPException(status_code=500, detail="Error guardando la cita")

    # 3. Obtener datos del vehículo para el mensaje (Marca y Modelo)
    vehicle = db.query(Vehicle).filter(Vehicle.id == booking.vehicle_id).first()
    vehicle_str = (
        f"{vehicle.brand} {vehicle.model} ({vehicle.year})"
        if vehicle
        else "Vehículo seleccionado"
    )

    # 4. Enviar WhatsApp (Si todo salió bien - Status 200 implícito al retornar)
    # Usamos background_tasks para que el usuario no espere a que Twilio responda
    background_tasks.add_task(
        whatsapp_service.send_appointment_confirmation,
        to_number=booking.customer_phone,
        user_name=booking.customer_name,
        date_str=booking.date.strftime("%d/%m/%Y a las %H:%M"),
        vehicle_info=vehicle_str,
    )

    return {"status": "success", "msg": "Cita creada y notificación enviada"}
