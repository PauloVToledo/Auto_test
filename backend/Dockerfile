# 1. Imagen base (Python 3.13 según tu estructura)
FROM python:3.13-slim

# 2. Variables de entorno para optimizar Python en Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema (necesarias para psycopg2/Postgres)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalar dependencias de Python
# Copiamos solo el requirements primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar TODO el código fuente
# (Gracias al .dockerignore, esto ignora venv y __pycache__)
COPY . .

# 7. Credenciales (Opcional si COPY . . ya lo hizo, pero seguro dejarlo)
# Asegúrate de que estos archivos existan localmente antes de construir
COPY credentials.json .
COPY token.json .

COPY restore_tokens.py .

# 8. Exponer puerto y comando de inicio
EXPOSE 8000

# CMD ejecuta el script de restauración PRIMERO y luego arranque la app
CMD python restore_tokens.py && uvicorn app.main:app --host 0.0.0.0 --port 8000