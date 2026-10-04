from __future__ import annotations
import math
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class SunPosition:
    altitude_deg: float
    azimuth_deg: float
    daylight: bool

def position(dt: datetime, latitude_deg: float, longitude_deg: float, utc_offset_hours: float) -> SunPosition:
    """Low-order deterministic solar-position approximation for v0.1 experiments."""
    if not -90 <= latitude_deg <= 90:
        raise ValueError("latitude must be between -90 and 90 degrees")
    if not -180 <= longitude_deg <= 180:
        raise ValueError("longitude must be between -180 and 180 degrees")
    if not -14 <= utc_offset_hours <= 14:
        raise ValueError("utc offset is outside supported range")
    n = dt.timetuple().tm_yday
    hour = dt.hour + dt.minute / 60 + dt.second / 3600
    b = math.radians(360 / 365 * (n - 81))
    eot = 9.87 * math.sin(2*b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
    solar_minutes = hour * 60 + eot + 4 * (longitude_deg - 15 * utc_offset_hours)
    ha = math.radians(solar_minutes / 4 - 180)
    dec = math.radians(23.44 * math.sin(math.radians(360 / 365 * (n - 81))))
    lat = math.radians(latitude_deg)
    sin_alt = math.sin(lat)*math.sin(dec) + math.cos(lat)*math.cos(dec)*math.cos(ha)
    altitude = math.degrees(math.asin(max(-1, min(1, sin_alt))))
    az = math.degrees(math.atan2(
        math.sin(ha),
        math.cos(ha)*math.sin(lat) - math.tan(dec)*math.cos(lat)
    ))
    azimuth = (az + 180) % 360
    return SunPosition(altitude, azimuth, altitude > 0)
