from blindlab.geometry import Vec3,Ray,Slat,ray_hits_slat,sun_direction
from blindlab.model import Blind
from blindlab.solar import SunPosition
from blindlab.experiment import geometry_validation

def test_ray_hits_finite_slat():
    assert ray_hits_slat(Ray(Vec3(0,-2,0),Vec3(0,1,0)),Slat(Vec3(0,0,0),Vec3(0,-1,0),1,1))

def test_parallel_ray_misses():
    assert not ray_hits_slat(Ray(Vec3(0,-2,0),Vec3(1,0,0)),Slat(Vec3(0,0,0),Vec3(0,-1,0),1,1))

def test_sun_direction_is_unit():
    assert abs(sun_direction(45,180).norm()-1)<1e-9

def test_geometry_validation_is_bounded():
    r=geometry_validation(Blind(45),SunPosition(50,180,True))
    assert 0<=r["ray_hits"]<=r["slat_count"]
