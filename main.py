from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import models
import database
import utils


app = FastAPI()

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- GPS ingestion ---
from pydantic import BaseModel

class GPSIn(BaseModel):
    device_id: str
    lat: float
    lon: float
    speed: float
    ts: datetime

@app.post("/ingest_gps")
def ingest_gps(gps: GPSIn, db: Session = Depends(get_db)):
    reason = utils.check_anomaly(gps.device_id, gps.lat, gps.lon, gps.speed, gps.ts)
    if reason:
        anomaly = models.Anomaly(device_id=gps.device_id, reason=reason, payload=gps.json())
        db.add(anomaly)
        gps_point = models.GPSPoint(device_id=gps.device_id, lat=gps.lat, lon=gps.lon,
                                    speed=gps.speed, ts=gps.ts, raw_flag=True)
    else:
        gps_point = models.GPSPoint(device_id=gps.device_id, lat=gps.lat, lon=gps.lon,
                                    speed=gps.speed, ts=gps.ts, raw_flag=False)
        # Challan rule (speed > 60 km/h for demo)
        if gps.speed > 60:
            challan = models.Challan(device_id=gps.device_id,
                                     speed=gps.speed, speed_limit=60,
                                     location=f"{gps.lat},{gps.lon}")
            db.add(challan)
    db.add(gps_point)
    utils.update_last_point(gps.device_id, gps.lat, gps.lon, gps.ts)
    db.commit()
    return {"status": "ok", "anomaly": reason}

# --- SOS ---
class SOSIn(BaseModel):
    device_id: str
    lat: float
    lon: float
    ts: datetime

@app.post("/sos")
def sos_alert(sos: SOSIn, db: Session = Depends(get_db)):
    alert = models.SOSAlert(device_id=sos.device_id, lat=sos.lat, lon=sos.lon, ts=sos.ts)
    db.add(alert)
    db.commit()
    return {"status": "sos_received"}

# --- List endpoints ---
@app.get("/challans")
def list_challans(db: Session = Depends(get_db)):
    return db.query(models.Challan).all()

@app.get("/anomalies")
def list_anomalies(db: Session = Depends(get_db)):
    return db.query(models.Anomaly).all()

@app.get("/sos_alerts")
def list_sos(db: Session = Depends(get_db)):
    return db.query(models.SOSAlert).all()
