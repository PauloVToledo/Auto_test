from app.core.database import SessionLocal, engine, Base
from app.models.vehicle import Vehicle
from app.models.appointment import (
    Appointment,
)  # Importar para que SQLAlchomy reconozca las relaciones


def seed_data():
    # 1. Crear las tablas (IMPORTANTE: Esto crea la estructura en la BD vacía de Docker)
    print("🛠️  Creando tablas en la Base de Datos...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # 2. Verificar si ya hay datos
    if db.query(Vehicle).first():
        print("⚠️  La base de datos ya tiene vehículos. Saltando seed.")
        return

    print("🌱 Sembrando datos de prueba...")

    # 3. Lista de Vehículos
    vehicles = [
        Vehicle(
            brand="Toyota",
            model="Corolla",
            year=2021,
            price=15000000,
            mileage=35000,
            color="Blanco",
        ),
        Vehicle(
            brand="Toyota",
            model="Hilux",
            year=2023,
            price=32000000,
            mileage=12000,
            color="Rojo",
        ),
        Vehicle(
            brand="Ford",
            model="Mustang",
            year=2020,
            price=45000000,
            mileage=8000,
            color="Negro",
        ),
        Vehicle(
            brand="Ford",
            model="Raptor",
            year=2022,
            price=55000000,
            mileage=15000,
            color="Azul",
        ),
        Vehicle(
            brand="Chevrolet",
            model="Camaro",
            year=2019,
            price=38000000,
            mileage=22000,
            color="Amarillo",
        ),
        Vehicle(
            brand="Chevrolet",
            model="Silverado",
            year=2021,
            price=42000000,
            mileage=30000,
            color="Gris",
        ),
        Vehicle(
            brand="Dodge",
            model="Challenger",
            year=2022,
            price=48000000,
            mileage=5000,
            color="Naranja",
        ),
        Vehicle(
            brand="BMW",
            model="X5",
            year=2021,
            price=60000000,
            mileage=25000,
            color="Negro",
        ),
    ]

    db.add_all(vehicles)
    db.commit()
    print("✅ ¡Vehículos insertados correctamente!")
    db.close()


if __name__ == "__main__":
    seed_data()
