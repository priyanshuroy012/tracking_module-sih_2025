from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class GPSPoint(Base):
    __tablename__ = "gps_points"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    lat = Column(Float)
    lon = Column(Float)
    speed = Column(Float)
    ts = Column(DateTime, default=datetime.utcnow)
    raw_flag = Column(Boolean, default=False)  # True if anomaly

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)
    reason = Column(String)
    payload = Column(String)

class Challan(Base):
    __tablename__ = "challans"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)
    speed = Column(Float)
    speed_limit = Column(Float)
    location = Column(String)
    paid = Column(Boolean, default=False)

class SOSAlert(Base):
    __tablename__ = "sos_alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)
    lat = Column(Float)
    lon = Column(Float)
    status = Column(String, default="active")
