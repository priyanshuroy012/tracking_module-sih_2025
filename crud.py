from sqlalchemy.orm import Session
import models, schemas

def get_buses(db: Session):
    return db.query(models.Bus).all()

# Mock ETA logic for now
def get_eta(db: Session):
    return [
        {"bus_id": 1, "stop_name": "Connaught Place", "arrival_time": 5},
        {"bus_id": 2, "stop_name": "Karol Bagh", "arrival_time": 12},
    ]

# Mock Carbon logic for now
def get_carbon(db: Session):
    return [
        {"metric": "Distance Travelled", "value": 120},
        {"metric": "Idle Time Saved", "value": 40},
        {"metric": "Eco Driving Score", "value": 75},
    ]
