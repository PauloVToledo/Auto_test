import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Si modificas los scopes, borra el archivo token.json
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
SELLER_EMAIL = os.getenv("MAIL_TO_SELLER")


def _get_gmail_service():
    """Autentica y retorna el servicio de la API de Gmail."""
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario.
    # Se crea automáticamente cuando el flujo de autorización se completa por primera vez.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Si no hay credenciales válidas disponibles, deja que el usuario inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # IMPORTANTE: Esto abrirá una ventana en tu navegador la primera vez
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardar las credenciales para la próxima ejecución
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def _create_html_template(client_name, client_phone, date, vehicle_info):
    """Plantilla HTML (Reutilizada)"""
    return f"""
    <div style="font-family: Arial, sans-serif; color: #333; border: 1px solid #ddd; padding: 20px;">
        <h2 style="color: #d93025;">📧 Nueva Cita (Gmail API)</h2>
        <p><strong>Cliente:</strong> {client_name}</p>
        <p><strong>Teléfono:</strong> <a href="https://wa.me/{client_phone.replace('+', '')}">{client_phone}</a></p>
        <p><strong>Auto:</strong> {vehicle_info}</p>
        <p><strong>Fecha:</strong> {date}</p>
        <hr>
        <small>Enviado desde el sistema de Automotora.</small>
    </div>
    """


def send_seller_notification(client_name, client_phone, date_str, vehicle_info):
    """Función principal para enviar el correo."""
    try:
        service = _get_gmail_service()

        # 1. Construir el mensaje MIME
        message = MIMEMultipart()
        message["to"] = SELLER_EMAIL
        message["subject"] = f"🔔 Cita: {client_name} - {vehicle_info}"

        html_content = _create_html_template(
            client_name, client_phone, date_str, vehicle_info
        )
        msg = MIMEText(html_content, "html")
        message.attach(msg)

        # 2. Codificar para Gmail API (Base64 URL Safe)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        body = {"raw": raw_message}

        # 3. Enviar
        sent_message = service.users().messages().send(userId="me", body=body).execute()
        print(f"📧 Gmail enviado correctamente! ID: {sent_message['id']}")

    except Exception as e:
        print(f"❌ Error enviando Gmail: {e}")
