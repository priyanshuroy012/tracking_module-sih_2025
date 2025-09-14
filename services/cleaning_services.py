def clean_gps_data(latitude, longitude, speed, last_point=None):
    """
    Basic cleaning rules:
    - Remove impossible speeds
    - Remove teleport jumps
    """
    if speed > 120:  # too fast for city bus
        return None

    if last_point:
        dist = ((latitude - last_point.latitude)**2 + (longitude - last_point.longitude)**2)**0.5
        if dist > 0.05:  # ~5km jump
            return None

    return {
        "latitude": latitude,
        "longitude": longitude,
        "speed": speed
    }
