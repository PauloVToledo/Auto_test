import os
from sqlalchemy import create_engine  # <--- Fíjate que NO diga create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# HACK: Si por casualidad tu .env sigue diciendo +asyncpg, esto lo arregla forzosamente:
if DATABASE_URL and "+asyncpg" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")

# Motor Síncrono
engine = create_engine(DATABASE_URL)

# Sesión Síncrona
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
