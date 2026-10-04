"""Generate the first BlindLab film with a local Wan2.2 backend.

Designed for a Linux NVIDIA self-hosted GitHub Actions runner. It intentionally
fails closed when the required model/runtime is unavailable.
"""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

from blindlab.studio import build_shot_manifest, validate_manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="artifacts/blindlab_studio")
    p.add_argument("--model-dir", default=os.environ.get("WAN_MODEL_DIR", "models/Wan2.2-TI2V-5B"))
    p.add_argument("--wan-repo", default=os.environ.get("WAN_REPO", "vendor/Wan2.2"))
    args = p.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    manifest = build_shot_manifest(str(out))
    validate_manifest(str(manifest))

    wan_generate = Path(args.wan_repo) / "generate.py"
    if not wan_generate.exists():
        raise SystemExit(f"Wan2.2 backend missing: {wan_generate}")
    if not Path(args.model_dir).exists():
        raise SystemExit(f"Wan2.2 model directory missing: {args.model_dir}")
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required")

    shots = json.loads(manifest.read_text(encoding="utf-8"))["shots"]
    generated = []
    for shot in shots:
        shot_dir = out / f"shot_{shot['id']}"
        shot_dir.mkdir(exist_ok=True)
        prompt_file = shot_dir / "prompt.txt"
        prompt_file.write_text(shot["prompt"], encoding="utf-8")
        cmd = [
            "python", str(wan_generate),
            "--task", "ti2v-5B",
            "--size", "1280*704",
            "--ckpt_dir", args.model_dir,
            "--offload_model", "True",
            "--convert_model_dtype",
            "--t5_cpu",
            "--prompt", shot["prompt"],
            "--save_file", str(shot_dir / "clip.mp4"),
        ]
        print("Generating", shot["id"])
        subprocess.run(cmd, check=True)
        generated.append(shot_dir / "clip.mp4")

    # The end card is deliberately deterministic rather than AI-generated.
    end_card = out / "end_card.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i",
        "color=c=black:s=1280x704:r=24", "-t", "2",
        "-vf", "drawtext=text='BLINDLAB':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2",
        "-pix_fmt", "yuv420p", str(end_card),
    ], check=True)

    concat = out / "concat.txt"
    with concat.open("w", encoding="utf-8") as f:
        for clip in generated:
            f.write(f"file '{clip.resolve()}'\\n")
        f.write(f"file '{end_card.resolve()}'\\n")

    final = out / "blindlab_reality_has_a_glitch.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-c", "copy", str(final)
    ], check=True)
    print(final)


if __name__ == "__main__":
    main()
