from geopy.distance import geodesic
from datetime import datetime

# In-memory last point cache
last_points = {}

def check_anomaly(device_id, lat, lon, speed, ts):
    """
    Simple rule-based anomaly detection.
    Returns reason if anomaly else None.
    """
    # Rule 1: Speed too high
    if speed > 200:
        return "speed_too_high"

    # Rule 2: Big GPS jump
    prev = last_points.get(device_id)
    if prev:
        prev_lat, prev_lon, prev_ts = prev
        dist_km = geodesic((prev_lat, prev_lon), (lat, lon)).km
        dt = (ts - prev_ts).total_seconds()
        if dt > 0 and dist_km / dt > 0.2:  # >200m per sec (~720 km/h)
            return "gps_jump"

    # TODO: stuck sensor rule (same point > 10min)
    return None

def update_last_point(device_id, lat, lon, ts):
    last_points[device_id] = (lat, lon, ts)
