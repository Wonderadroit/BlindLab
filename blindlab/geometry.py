from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Vec3:
    x: float; y: float; z: float
    def dot(self, other:"Vec3")->float: return self.x*other.x+self.y*other.y+self.z*other.z
    def norm(self)->float: return math.sqrt(self.dot(self))
    def normalized(self)->"Vec3":
        n=self.norm()
        if n==0: raise ValueError("zero vector cannot be normalized")
        return Vec3(self.x/n,self.y/n,self.z/n)
    def __add__(self,o:"Vec3")->"Vec3": return Vec3(self.x+o.x,self.y+o.y,self.z+o.z)
    def __sub__(self,o:"Vec3")->"Vec3": return Vec3(self.x-o.x,self.y-o.y,self.z-o.z)
    def __mul__(self,s:float)->"Vec3": return Vec3(self.x*s,self.y*s,self.z*s)

@dataclass(frozen=True)
class Ray:
    origin: Vec3
    direction: Vec3

@dataclass(frozen=True)
class Slat:
    center: Vec3
    normal: Vec3
    half_width: float
    half_depth: float

def ray_hits_slat(ray:Ray, slat:Slat)->bool:
    d=ray.direction.normalized(); n=slat.normal.normalized()
    denom=d.dot(n)
    if abs(denom)<1e-9: return False
    t=(slat.center-ray.origin).dot(n)/denom
    if t<=0: return False
    p=ray.origin+d*t
    return abs(p.x-slat.center.x)<=slat.half_width+1e-9 and abs(p.z-slat.center.z)<=slat.half_depth+1e-9

def sun_direction(altitude_deg:float, azimuth_deg:float)->Vec3:
    a=math.radians(altitude_deg); z=math.radians(azimuth_deg)
    return Vec3(math.cos(a)*math.sin(z), math.cos(a)*math.cos(z), math.sin(a)).normalized()
