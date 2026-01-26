import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
SELLER_EMAIL = os.getenv("MAIL_TO_SELLER")


def _get_gmail_service():
    """Autenticación interna de Google"""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Nota: Asumimos que el token ya existe tras el primer login que hiciste
    if creds and creds.valid:
        return build("gmail", "v1", credentials=creds)
    return None


def _send_email_base(to_email, subject, html_content):
    """Función genérica para enviar cualquier correo"""
    try:
        service = _get_gmail_service()
        if not service:
            print("❌ Error: No hay credenciales válidas (token.json) para Gmail.")
            return

        message = MIMEMultipart()
        message["to"] = to_email
        message["subject"] = subject

        msg = MIMEText(html_content, "html")
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        body = {"raw": raw_message}

        service.users().messages().send(userId="me", body=body).execute()
        print(f"📧 Email enviado a {to_email}")

    except Exception as e:
        print(f"❌ Error enviando Gmail a {to_email}: {e}")


# --- CORREO PARA EL VENDEDOR (ADMIN) ---
def send_seller_notification(
    client_name, client_email, client_phone, date_str, vehicle_info
):
    html = f"""
    <div style="font-family: Arial; border: 1px solid #ccc; padding: 20px;">
        <h2 style="color: #d93025;">🔔 Nueva Venta Potencial</h2>
        <p>Un cliente ha agendado una visita.</p>
        <ul>
            <li><strong>Cliente:</strong> {client_name}</li>
            <li><strong>Email:</strong> {client_email}</li>
            <li><strong>Teléfono:</strong> {client_phone}</li>
            <li><strong>Auto:</strong> {vehicle_info}</li>
            <li><strong>Fecha:</strong> {date_str}</li>
        </ul>
    </div>
    """
    _send_email_base(SELLER_EMAIL, f"Nueva Cita: {client_name}", html)


# --- CORREO PARA EL CLIENTE (CONFIRMACIÓN) ---
def send_customer_confirmation(to_email, client_name, date_str, vehicle_info):
    html = f"""
    <div style="font-family: Arial; border: 1px solid #0d6efd; border-radius: 10px; padding: 20px; max-width: 600px;">
        <div style="text-align: center; color: #0d6efd;">
            <h1>¡Cita Confirmada! ✅</h1>
        </div>
        <p>Hola <strong>{client_name}</strong>,</p>
        <p>Gracias por tu interés en <strong>Automotora Pro</strong>. Tu visita ha sido agendada correctamente.</p>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 5px 0;">🚗 <strong>Vehículo:</strong> {vehicle_info}</p>
            <p style="margin: 5px 0;">📅 <strong>Cuándo:</strong> {date_str}</p>
            <p style="margin: 5px 0;">📍 <strong>Dónde:</strong> Av. Siempre Viva 123</p>
        </div>

        <p>Si necesitas cambiar la hora, contáctanos por WhatsApp.</p>
        <p>¡Te esperamos!</p>
    </div>
    """
    _send_email_base(to_email, "Confirmación de Visita - Automotora Pro", html)
