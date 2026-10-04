from pathlib import Path

def test_v03_renderer_exists_and_declares_boundary():
    text = Path("blender/scene_v03.py").read_text(encoding="utf-8")
    # Blender 4.0 exposes BLENDER_EEVEE; newer releases may expose
    # BLENDER_EEVEE_NEXT. The renderer must explicitly support either.
    assert "scene.render.engine=" in text
    assert "BLENDER_EEVEE" in text
    assert "BLENDER_EEVEE_NEXT" in text
    assert '"calibrated_photometry": false' in text
