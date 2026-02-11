import structlog
from unittest.mock import patch  # <--- Necesario para bloquear envíos reales
from structlog.testing import capture_logs
from app.core.logging import configure_logging

# Asegurarnos de que la config esté cargada
configure_logging()


def test_appointment_logs_structure(client, create_test_vehicle):
    """
    Verifica que al crear una cita, se generen logs estructurados (JSON)
    con los campos correctos (event, vehicle_id, etc).
    """

    vehicle_id = create_test_vehicle.id
    payload = {
        "vehicle_id": vehicle_id,
        "customer_name": "Log Tester",
        "customer_phone": "+56911112222",
        "date": "2023-12-25T12:00:00",
        "customer_email": "log@qa.com",
    }

    # 1. MOCKING: Evitamos que intente enviar WhatsApps o Correos reales
    with patch("app.services.whatsapp_service.send_appointment_confirmation"), patch(
        "app.services.gmail_service.send_seller_notification"
    ):

        # 2. CAPTURA DE LOGS
        with capture_logs() as cap_logs:
            response = client.post("/api/v1/appointments/", json=payload)

            assert response.status_code == 200

            # --- QA DE LOGS ---

            # Verificar que se generaron logs
            assert len(cap_logs) > 0, "No se generaron logs"

            # Buscar el log específico de "Guardado en BD"
            success_log = None
            for log in cap_logs:
                if log.get("event") == "appointment_saved_db":
                    success_log = log
                    break

            assert (
                success_log is not None
            ), "Falta el log de evento 'appointment_saved_db'"

            # Verificar datos de contexto
            assert success_log["vehicle_id"] == vehicle_id
            assert "appointment_id" in success_log

            # NOTA: Quitamos la validación de 'timestamp' porque capture_logs
            # intercepta el evento antes de que el procesador de tiempo actúe.

            # Verificar el log de inicio (donde inyectamos el teléfono)
            start_log = [
                l for l in cap_logs if l.get("event") == "appointment_request_received"
            ][0]
            assert start_log["customer_phone"] == "+56911112222"
            assert start_log["msg"] == "Iniciando proceso de reserva"
