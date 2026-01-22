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

# Copiar el código
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para correr la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]