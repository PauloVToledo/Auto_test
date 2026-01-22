from fastapi import APIRouter
from app.api.v1.endpoints import vehicles
from app.api.v1.endpoints import vehicles, appointments, chat

api_router = APIRouter()

# Aquí es donde importarás tus futuros endpoints.
# Ejemplo: api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])

# Add the router
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])


api_router.include_router(
    appointments.router, prefix="/appointments", tags=["appointments"]
)

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
