from pathlib import Path

def test_v03_renderer_exists_and_declares_boundary():
    text = Path("blender/scene_v03.py").read_text(encoding="utf-8")
    assert 'scene.render.engine = "BLENDER_EEVEE"' in text
    assert 'scene.render.engine = "BLENDER_EEVEE_NEXT"' in text
    assert '"calibrated_photometry": false' in text
