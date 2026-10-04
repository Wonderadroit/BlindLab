from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime
import math
from .model import Blind, ExperimentWeights, Window
from .solar import SunPosition

@dataclass(frozen=True)
class CandidateScore:
    angle_deg: float
    daylight: float
    privacy: float
    heat: float
    total: float

def _angular_distance(a: float, b: float) -> float:
    return abs((a - b + 180) % 360 - 180)

def score_candidate(blind: Blind, window: Window, sun: SunPosition, weights: ExperimentWeights) -> CandidateScore:
    """Inspectable v0.1 geometry proxy, not a calibrated physical model."""
    if not sun.daylight or sun.altitude_deg <= 0:
        return CandidateScore(blind.slat_angle_deg, 1.0, 1.0, 0.0, weights.daylight + weights.privacy)
    incidence = _angular_distance(sun.azimuth_deg, window.azimuth_deg)
    facing = max(0.0, math.cos(math.radians(incidence)))
    closure = blind.slat_angle_deg / 90.0
    daylight = max(0.0, min(1.0, (1 - 0.72*closure) * (1 - 0.55*facing*math.sin(math.radians(sun.altitude_deg)))))
    privacy = max(0.0, min(1.0, 0.15 + 0.85*closure))
    heat = max(0.0, min(1.0, facing*math.sin(math.radians(sun.altitude_deg))*(1 - 0.85*closure)))
    total = weights.daylight*daylight + weights.privacy*privacy + weights.heat*(1-heat)
    return CandidateScore(blind.slat_angle_deg, daylight, privacy, heat, total)

def sweep_angles(window, sun, weights, start_deg=0, stop_deg=90, step_deg=5):
    if step_deg <= 0:
        raise ValueError("step must be positive")
    if stop_deg < start_deg:
        raise ValueError("stop must be >= start")
    count = int(round((stop_deg-start_deg)/step_deg))
    return [score_candidate(Blind(slat_angle_deg=start_deg+i*step_deg), window, sun, weights)
            for i in range(count+1)]

def choose_best(candidates):
    if not candidates:
        raise ValueError("candidate set cannot be empty")
    return max(candidates, key=lambda c: (c.total, -c.angle_deg))

def report(dt, latitude_deg, longitude_deg, utc_offset_hours, window, sun, weights, candidates, best):
    return {
        "schema":"blindlab.experiment.v0.1",
        "timestamp":dt.isoformat(),
        "location":{"latitude_deg":latitude_deg,"longitude_deg":longitude_deg,"utc_offset_hours":utc_offset_hours},
        "window":asdict(window),"sun":asdict(sun),"weights":asdict(weights),
        "candidate_count":len(candidates),"best":asdict(best),
        "candidates":[asdict(c) for c in candidates],
        "limitations":[
            "Solar position is a low-order approximation.",
            "Daylight/privacy/heat are normalized geometry proxies, not calibrated measurements.",
            "No room materials, glass transmission, diffuse sky light, or thermal mass are modeled."
        ]
    }
