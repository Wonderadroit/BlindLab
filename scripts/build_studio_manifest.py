from blindlab.studio import build_shot_manifest, validate_manifest

path = build_shot_manifest()
validate_manifest(str(path))
print(path)
