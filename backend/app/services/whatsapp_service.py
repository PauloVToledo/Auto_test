import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Cargar variables globales
SID = os.getenv("TWILIO_ACCOUNT_SID")
TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def send_appointment_confirmation(
    to_number: str, user_name: str, date_str: str, vehicle_info: str
):
    """
    Envía confirmación de cita por WhatsApp.
    """
    try:
        if not SID or not TOKEN:
            print("❌ ERROR: Faltan credenciales de Twilio en .env")
            return

        client = Client(SID, TOKEN)

        to_number = "whatsapp:+56966328107"
        # Twilio Sandbox requiere el prefijo 'whatsapp:' en ambos números
        # Asegúrate de que to_number venga con formato internacional (ej: +569...)
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"

        message_body = (
            f"🚗 *¡Hola {user_name}!* \n\n"
            f"Tu visita ha sido agendada con éxito. ✅\n\n"
            f"📅 *Fecha:* {date_str}\n"
            f"🚙 *Vehículo:* {vehicle_info}\n\n"
            f"Te esperamos en la sucursal ubicada en la Dirección 'Tester 123'. ¡Saludos!"
        )

        message = client.messages.create(
            from_=FROM_NUMBER, body=message_body, to=to_number
        )

        print(f"✅ WhatsApp enviado. ID: {message.sid}")

    except Exception as e:
        print(f"❌ Error enviando WhatsApp: {e}")
