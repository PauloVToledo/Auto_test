import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Si modificas estos alcances, elimina tu token.json anterior.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
# OJO: Asegúrate de que este SCOPE sea el mismo que usas en tu app real.


def main():
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario.
    # Si existe uno viejo o expirado, bórralo manualmente antes de correr esto.
    if os.path.exists("token.json"):
        os.remove("token.json")  # Lo borramos para forzar uno nuevo

    # Flujo para loguearse
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                print("No se pudo refrescar, logueando de nuevo...")
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)

            # IMPORTANTE: access_type='offline' garantiza que nos den un refresh_token
            # prompt='consent' fuerza a Google a preguntar permisos de nuevo para asegurar el refresh_token
            creds = flow.run_local_server(
                port=0, access_type="offline", prompt="consent"
            )

        # Guardar las credenciales para la próxima ejecución
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    print("✅ ¡Nuevo token.json generado con éxito!")

    # Imprimimos el contenido para que lo copies fácil a Render
    with open("token.json", "r") as f:
        content = f.read()
        print("\n👇 COPIA TODO ESTO A TU VARIABLE DE ENTORNO EN RENDER 👇\n")
        print(content)


if __name__ == "__main__":
    main()
