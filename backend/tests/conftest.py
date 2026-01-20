import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db

# 1. Configurar DB temporal en memoria (SQLite)
# Esto simula tu Postgres pero vive solo durante el test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 2. Fixture para sobreescribir la dependencia de la DB
# Cuando la app pida 'get_db', le daremos esta DB falsa
@pytest.fixture(scope="function")
def override_get_db():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Borrar tablas al terminar
        Base.metadata.drop_all(bind=engine)


# 3. Fixture del Cliente HTTP
# Este es el "navegador" falso que usaremos para llamar a la API
@pytest.fixture(scope="function")
def client(override_get_db):
    # Sobreescribir la dependencia original
    app.dependency_overrides[get_db] = lambda: override_get_db
    with TestClient(app) as c:
        yield c
    # Limpiar overrides
    app.dependency_overrides.clear()


# 4. Fixture para crear un vehículo de prueba
# Útil para no repetir código en cada test
@pytest.fixture
def create_test_vehicle(override_get_db):
    from app.models.vehicle import Vehicle

    vehicle = Vehicle(
        brand="TestBrand",
        model="TestModel",
        year=2024,
        price=10000,
        mileage=500,
        color="White",
    )
    override_get_db.add(vehicle)
    override_get_db.commit()
    override_get_db.refresh(vehicle)
    return vehicle
