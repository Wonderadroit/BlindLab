"""BlindLab self-hosted photorealistic production orchestration.

This module owns the production contract. The actual generative model is an
interchangeable local/open-weight backend; BlindLab never treats generated
pixels as physical evidence.
"""

from dataclasses import asdict
from pathlib import Path
import json

from .creative import FIRST_FILM, production_prompt


def build_shot_manifest(output_dir: str = "artifacts/blindlab_studio") -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    shots = []
    for shot in FIRST_FILM[:4]:
        shots.append({
            **asdict(shot),
            "prompt": production_prompt(shot),
            "negative_prompt": (
                "CGI, 3D render, videogame, plastic skin, waxy face, synthetic anatomy, "
                "floating objects, impossible shadows, inconsistent reflections, neon UI, "
                "oversharpened, cartoon, illustration, low detail, deformed hands"
            ),
        })
    path = out / "shot_manifest.json"
    path.write_text(json.dumps({
        "schema": "blindlab.studio.manifest.v0.1",
        "film": "Reality Has a Glitch",
        "duration_s": 15.0,
        "backend": "self-hosted-open-weight",
        "shots": shots,
    }, indent=2), encoding="utf-8")
    return path


def validate_manifest(path: str) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == "blindlab.studio.manifest.v0.1"
    assert data["backend"] == "self-hosted-open-weight"
    assert len(data["shots"]) == 4
    assert sum(s["duration_s"] for s in data["shots"]) == 13.0
    for shot in data["shots"]:
        assert "Photorealistic cinematic frame" in shot["prompt"]
        assert "Do not make it look like CGI" in shot["prompt"]
        assert shot["negative_prompt"]
