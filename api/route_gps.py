from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.gps_point import GPSPoint
from services.cleaning_services import clean_gps_data

router = APIRouter(prefix="/gps", tags=["GPS"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ingest")
def ingest_gps(trip_id: int, latitude: float, longitude: float, speed: float, db: Session = Depends(get_db)):
    # Clean incoming data
    cleaned = clean_gps_data(latitude, longitude, speed)
    if not cleaned:
        return {"status": "discarded", "reason": "anomalous data"}

    gps_point = GPSPoint(
        trip_id=trip_id,
        latitude=cleaned["latitude"],
        longitude=cleaned["longitude"],
        speed=cleaned["speed"]
    )
    db.add(gps_point)
    db.commit()
    return {"status": "stored", "point_id": gps_point.id}
