from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.vehicle import Vehicle

router = APIRouter()


@router.get("")
def read_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()
