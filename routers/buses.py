from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import get_buses
import schemas
from database import get_db
from typing import List

router = APIRouter(prefix="/api/buses", tags=["buses"])

@router.get("/", response_model=List[schemas.BusOut])
def read_buses(db: Session = Depends(get_db)):
    return get_buses(db)
