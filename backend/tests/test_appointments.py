from unittest.mock import patch


def test_create_appointment_success(client, create_test_vehicle):
    """
    Debe crear una cita en BD y llamar a las tareas de background (Mocks)
    """
    vehicle_id = create_test_vehicle.id

    payload = {
        "vehicle_id": vehicle_id,
        "customer_name": "Tester QA",
        "customer_phone": "+56999999999",
        "date": "2023-12-25T10:00:00",
    }

    # MOCKING: "Parcheamos" los servicios externos.
    # Le decimos a Python: "Cuando alguien intente llamar a whatsapp_service.send...,
    # no hagas nada real, solo anota que te llamaron".
    with patch(
        "app.services.whatsapp_service.send_appointment_confirmation"
    ) as mock_whatsapp, patch(
        "app.services.gmail_service.send_seller_notification"
    ) as mock_gmail:

        # 1. Ejecutar la petición
        response = client.post("/api/v1/appointments/", json=payload)

        # 2. Validar Respuesta HTTP
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        # 3. Validar Mocks (¿Se intentó enviar el mensaje?)
        # Como usamos BackgroundTasks, en los tests síncronos a veces hay que forzar
        # la ejecución o confiar en que la lógica pasó por ahí.
        # Nota: FastAPI TestClient ejecuta BackgroundTasks automáticamente al finalizar el request.

        mock_whatsapp.assert_called_once()
        mock_gmail.assert_called_once()

        # --- CORRECCIÓN AQUÍ ---
        # No usamos 'args' porque enviaste los datos como 'user_name=...' (kwargs)
        # Accedemos directamente al diccionario de argumentos llamados.
        called_kwargs = mock_whatsapp.call_args.kwargs

        assert called_kwargs["user_name"] == "Tester QA"
        assert called_kwargs["to_number"] == "+56999999999"


def test_create_appointment_invalid_data(client):
    """Debe fallar si faltan datos obligatorios"""
    payload = {
        "vehicle_id": 1,
        # Falta el teléfono y el nombre
        "date": "2023-12-25T10:00:00",
    }
    response = client.post("/api/v1/appointments/", json=payload)
    assert (
        response.status_code == 422
    )  # Unprocessable Entity (Error de validación Pydantic)
