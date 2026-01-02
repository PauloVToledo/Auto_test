from fastapi import APIRouter
from app.api.v1.endpoints import vehicles

api_router = APIRouter()

# Aquí es donde importarás tus futuros endpoints.
# Ejemplo: api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])

# Add the router
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])


# @api_router.get("/test")
# def test_route():
#     return {"msg": "El router API v1 está funcionando correctamente"}
