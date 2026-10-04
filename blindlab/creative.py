"""BlindLab photorealistic production blueprint.

This module describes shots for human-led/AI-assisted image and video production.
It deliberately does not claim that generated imagery is photographic evidence.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Shot:
    id: str
    duration_s: float
    location: str
    action: str
    camera: str
    lighting: str
    realism_checks: Tuple[str, ...]


REALISM_RULES = (
    "photographic human anatomy and skin texture",
    "physically plausible lighting and reflections",
    "natural lens depth of field and motion blur",
    "real materials with small imperfections",
    "no 3D-rendered or videogame appearance",
    "no holograms or synthetic UI unless explicitly part of the concept",
)


FIRST_FILM = (
    Shot(
        "01",
        3.0,
        "ordinary Lagos street at golden hour",
        "A person walks naturally through everyday traffic and pedestrians.",
        "35mm full-frame cinema look; slow, stable push-in",
        "real sun, ambient bounce, practical street light",
        REALISM_RULES,
    ),
    Shot(
        "02",
        3.0,
        "same location",
        "A mundane object begins behaving impossibly while the environment remains ordinary.",
        "50mm; subtle rack focus from subject to object",
        "unchanged natural light; believable shadows and reflections",
        REALISM_RULES,
    ),
    Shot(
        "03",
        4.0,
        "same location",
        "The impossible event becomes undeniable without changing the photographic reality of the scene.",
        "85mm; controlled handheld micro-movement",
        "natural contrast; restrained cinematic grade",
        REALISM_RULES,
    ),
    Shot(
        "04",
        3.0,
        "same location, wider view",
        "A wider reveal shows the scale of the phenomenon.",
        "24mm; slow physical dolly/reveal",
        "consistent sun direction and exposure",
        REALISM_RULES,
    ),
    Shot(
        "05",
        2.0,
        "black / minimal end card",
        "BlindLab identity appears cleanly.",
        "static",
        "minimal",
        ("clean typography",),
    ),
)


def production_prompt(shot: Shot) -> str:
    """Return a vendor-neutral prompt for a photorealistic keyframe."""
    checks = "; ".join(shot.realism_checks)
    return (
        f"Photorealistic cinematic frame for BlindLab, shot {shot.id}. "
        f"Location: {shot.location}. Action: {shot.action} "
        f"Camera: {shot.camera}. Lighting: {shot.lighting}. "
        f"Priority: {checks}. "
        "Premium commercial cinematography, authentic imperfections, "
        "natural skin and materials, realistic exposure, physically plausible optics. "
        "Do not make it look like CGI, 3D, illustration, game footage, or a synthetic render."
    )
