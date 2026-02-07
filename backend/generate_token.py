from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Los permisos que necesitamos (Enviar correo)
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main():
    # Verificar que existe el archivo credentials.json
    if not os.path.exists("credentials.json"):
        print("❌ Error: No se encuentra el archivo 'credentials.json'.")
        print("Descárgalo de Google Cloud Console y ponlo en esta carpeta.")
        return

    # Iniciar flujo de OAuth (Se abrirá el navegador)
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Guardar el token generado
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    print("✅ ¡token.json generado con éxito! Ahora puedes enviar correos.")


if __name__ == "__main__":
    main()
