# Usar imagen ligera de Python
FROM python:3.13-slim

# Evitar que Python genere archivos .pyc y buffer de salida
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y gcc libpq-dev

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .


# ✅ ASEGÚRATE DE QUE ESTO ESTÉ:
COPY restore_tokens.py .

# Exponer el puerto
EXPOSE 8000

# Comando: Ejecuta el script de restauración PRIMERO, luego arranca la app
CMD python restore_tokens.py && python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000