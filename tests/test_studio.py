from blindlab.studio import build_shot_manifest, validate_manifest

def test_studio_manifest(tmp_path):
    path = build_shot_manifest(str(tmp_path))
    validate_manifest(str(path))
