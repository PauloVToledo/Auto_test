import os


def restore_file_from_env(env_var_name, file_name):
    content = os.getenv(env_var_name)
    if content:
        print(f"🔄 Restaurando {file_name} desde variables de entorno...")
        with open(file_name, "w") as f:
            f.write(content)
    else:
        print(
            f"⚠️ Variable {env_var_name} no encontrada. Se asume que el archivo {file_name} ya existe o no se necesita."
        )


if __name__ == "__main__":
    # Restaurar token de Gmail
    restore_file_from_env("GOOGLE_TOKEN_JSON_CONTENT", "token.json")

    # Restaurar credenciales (si fuera necesario, aunque suele ser estático)
    # restore_file_from_env("GOOGLE_CREDENTIALS_JSON_CONTENT", "credentials.json")
