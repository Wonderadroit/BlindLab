from __future__ import annotations
from dataclasses import asdict
from .geometry import Ray, Slat, Vec3, ray_hits_slat, sun_direction
from .model import Blind
from .solar import SunPosition

def slat_normal(angle_deg:float)->Vec3:
    # Rotation about x: a horizontal slat tilted toward/away from the room.
    a=__import__("math").radians(angle_deg)
    return Vec3(0, -__import__("math").sin(a), __import__("math").cos(a)).normalized()

def geometry_validation(blind:Blind, sun:SunPosition)->dict:
    """Construct the same conceptual slat stack used by the Blender scene and test a sun ray."""
    direction=sun_direction(sun.altitude_deg,sun.azimuth_deg)
    origin=Vec3(0, -4, blind.window_height_m/2)
    hits=0
    for i in range(blind.slat_count):
        z=(i+0.5)*blind.window_height_m/blind.slat_count
        slat=Slat(Vec3(0,0,z),slat_normal(blind.slat_angle_deg),blind.window_width_m/2,blind.slat_depth_m/2)
        if ray_hits_slat(Ray(origin,direction),slat): hits+=1
    return {"ray_hits":hits,"slat_count":blind.slat_count,"sun_direction":asdict(direction),
            "geometry_model":"finite_slat_plane_v0.2"}
