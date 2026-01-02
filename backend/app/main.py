from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

from contextlib import asynccontextmanager
from app.core.database import engine, Base

# uvicorn app.main:app --reload   --> to run the app.

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
    # Aquí agregarás tu dominio real cuando despliegues (ej: https://mi-automotora.com)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Quién puede conectarse
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los headers
)

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
# ???
