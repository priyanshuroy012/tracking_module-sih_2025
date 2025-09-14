from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BusBase(BaseModel):
    name: str
    lat: float
    lon: float
    speed: float

class BusCreate(BusBase):
    pass

class BusOut(BusBase):
    id: int
    class Config:
        orm_mode = True

class ETA(BaseModel):
    bus_id: int
    stop_name: str
    arrival_time: int

class CarbonMetric(BaseModel):
    metric: str
    value: float
