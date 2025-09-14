from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import get_eta
from database import get_db

router = APIRouter(prefix="/api/eta", tags=["eta"])

@router.get("/")
def read_eta(db: Session = Depends(get_db)):
    return get_eta(db)
