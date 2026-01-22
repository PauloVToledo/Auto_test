from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

from contextlib import asynccontextmanager
from app.core.database import engine, Base

from app.core.logging import configure_logging

import structlog
import time
import uuid


# 1. INICIAR EL LOGGER
configure_logging()
logger = structlog.get_logger()

# uvicorn app.main:app --reload   --> to run the app

# 1. Inicialización de la App
# Definimos el título y versión (útil para la documentación automática)
app = FastAPI(
    title="Automotora Booking API",
    description="API para agendamiento de citas y notificaciones WhatsApp",
    version="1.0.0",
    # openapi_url="/api/v1/openapi.json" # Descomentar en producción
)

# 2. Configuración de CORS (Cross-Origin Resource Sharing)
# Esto es CRUCIAL. Permite que tu Frontend (Next.js en el puerto 3000)
# pueda hablar con este Backend (en el puerto 8000).
origins = [
    "http://localhost:3000",  # Tu frontend en desarrollo
    "http://127.0.0.1:3000",
    "*",
    # Aquí agregarás tu dominio real cuando despliegues (ej: https://mi-automotora.com)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Quién puede conectarse
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los headers
)


# 2. MIDDLEWARE DE LOGGING (Interceptor)
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # Generar un ID único para esta petición (Tracing)
    request_id = str(uuid.uuid4())

    # Limpiar contexto previo y vincular el ID
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host,
    )

    start_time = time.time()

    try:
        # Ejecutar la petición real
        response = call_next(request)
        # Si es una corrutina (async), esperar
        if hasattr(response, "__await__"):
            response = await response

        process_time = time.time() - start_time

        # Loguear el resultado (SUCCESS)
        logger.info(
            "http_request",
            status_code=response.status_code,
            duration=round(process_time, 4),
        )
        return response

    except Exception as e:
        # Loguear errores no controlados (CRITICAL)
        process_time = time.time() - start_time
        logger.error(
            "http_request_failed", error=str(e), duration=round(process_time, 4)
        )
        raise e


# 3. Incluir las Rutas (Endpoints)
# Aquí conectamos toda la lógica de tus citas y WhatsApp
app.include_router(api_router, prefix="/api/v1")


# 4. Endpoint de "Health Check"
# Útil para saber si el servidor está vivo (ping)
@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API de la Automotora",
        "status": "running",
        "docs": "/docs",  # Indica dónde ver la documentación
    }


# 5. Configuración para Debugging (Opcional)
# Permite ejecutar el archivo directamente con python main.py
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
