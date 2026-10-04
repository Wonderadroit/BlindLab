from pathlib import Path
import re


def test_v03_renderer_exists_and_declares_boundary():
    text = Path("blender/scene_v03.py").read_text(encoding="utf-8")
    engines = set(re.findall(r'scene\\.render\\.engine\\s*=\\s*"([^"]+)"', text))
    assert {"BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"} <= engines
    assert '"calibrated_photometry": false' in text
