from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Blind:
    slat_angle_deg: float = 45.0
    slat_count: int = 24
    slat_depth_m: float = 0.025
    window_width_m: float = 1.2
    window_height_m: float = 1.5

    def __post_init__(self):
        if not 0 <= self.slat_angle_deg <= 90:
            raise ValueError("slat angle must be in [0, 90]")
        if self.slat_count < 1 or self.slat_depth_m <= 0:
            raise ValueError("slat geometry must be positive")
        if self.window_width_m <= 0 or self.window_height_m <= 0:
            raise ValueError("window dimensions must be positive")

@dataclass(frozen=True)
class ExperimentWeights:
    daylight: float = 0.55
    privacy: float = 0.25
    heat: float = 0.20

    def __post_init__(self):
        if min(self.daylight, self.privacy, self.heat) < 0:
            raise ValueError("weights cannot be negative")
        if self.daylight + self.privacy + self.heat <= 0:
            raise ValueError("at least one weight must be positive")

@dataclass(frozen=True)
class Window:
    azimuth_deg: float = 180.0

    def __post_init__(self):
        if not 0 <= self.azimuth_deg < 360:
            raise ValueError("window azimuth must be in [0, 360)")
