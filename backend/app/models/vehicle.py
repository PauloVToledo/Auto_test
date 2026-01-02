from sqlalchemy import Column, Integer, String, Float, BigInteger
from app.core.database import Base


class Vehicle(Base):
    # ¡OJO! Reemplaza "vehicles" por el nombre REAL de tu tabla si es distinto
    __tablename__ = "vehicles"

    # La columna nueva que acabamos de crear con SQL
    id = Column(Integer, primary_key=True, index=True)

    # Las columnas exactas de tu imagen
    # Usamos BigInteger para 'price' y 'year' porque en la imagen dicen 'bigint'
    price = Column(BigInteger)
    brand = Column(String)
    model = Column(String)
    year = Column(BigInteger)

    # 'double precision' en Postgres es Float en Python
    mileage = Column(Float)

    color = Column(String)

    def __repr__(self):
        return f"<Vehicle {self.brand} {self.model}>"
