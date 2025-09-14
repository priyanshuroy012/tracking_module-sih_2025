from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from database import get_db

router = APIRouter(prefix="/api/carbon", tags=["carbon"])

@router.get("/")
def read_carbon(db: Session = Depends(get_db)):
    return crud.get_carbon(db)
