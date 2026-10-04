"""Generate BlindLab's first film with a self-hosted Wan2.2 TI2V-5B backend.

Continuity strategy:
- Shot 01 is text-to-video.
- The final frame of each generated shot becomes the reference image for the next.
- This keeps the same environment/subject visually anchored without a commercial API.
- Generation fails closed if the local GPU/model/runtime is unavailable.
"""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

from blindlab.studio import build_shot_manifest, validate_manifest


def run(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, check=True)


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
    model_dir = Path(args.model_dir)
    if not model_dir.exists():
        raise SystemExit(f"Wan2.2 model directory missing: {model_dir}")
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required")

    shots = json.loads(manifest.read_text(encoding="utf-8"))["shots"]
    generated = []
    previous_frame = None

    for shot in shots:
        shot_dir = out / f"shot_{shot['id']}"
        shot_dir.mkdir(exist_ok=True)
        prompt_file = shot_dir / "prompt.txt"
        prompt_file.write_text(
            shot["prompt"] +
            "\nCONTINUITY LOCK: preserve the same people, clothing, vehicles, "
            "architecture, weather, sun direction, camera-world geometry and "
            "material appearance established by the reference frame.",
            encoding="utf-8",
        )

        frame_num = int(round(shot["duration_s"] * 24))
        # Wan requires frame_num = 4n + 1.
        frame_num = 4 * round((frame_num - 1) / 4) + 1
        clip = shot_dir / "clip.mp4"

        cmd = [
            "python", str(wan_generate),
            "--task", "ti2v-5B",
            "--size", "1280*704",
            "--frame_num", str(frame_num),
            "--ckpt_dir", str(model_dir),
            "--offload_model", "True",
            "--convert_model_dtype",
            "--t5_cpu",
            "--prompt", prompt_file.read_text(encoding="utf-8"),
            "--save_file", str(clip),
        ]
        if previous_frame is not None:
            cmd.extend(["--image", str(previous_frame)])

        print("Generating shot", shot["id"], "with", frame_num, "frames", flush=True)
        run(cmd)
        if not clip.exists() or clip.stat().st_size == 0:
            raise SystemExit(f"Generator did not produce {clip}")

        generated.append(clip)
        previous_frame = shot_dir / "last_frame.png"
        run([
            "ffmpeg", "-y", "-sseof", "-0.05", "-i", str(clip),
            "-frames:v", "1", "-update", "1", str(previous_frame)
        ])

    end_card = out / "end_card.mp4"
    run([
        "ffmpeg", "-y", "-f", "lavfi", "-i",
        "color=c=black:s=1280x704:r=24", "-t", "2",
        "-vf", "drawtext=text='BLINDLAB':fontcolor=white:fontsize=64:"
        "x=(w-text_w)/2:y=(h-text_h)/2",
        "-pix_fmt", "yuv420p", str(end_card),
    ])

    concat = out / "concat.txt"
    with concat.open("w", encoding="utf-8") as f:
        for clip in generated:
            f.write(f"file '{clip.resolve()}'\\n")
        f.write(f"file '{end_card.resolve()}'\\n")

    final = out / "blindlab_reality_has_a_glitch.mp4"
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-vf", "fps=24,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-movflags", "+faststart", str(final),
    ])

    # Machine gate: the film must be approximately 15 seconds.
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(final)
    ], text=True).strip()
    duration = float(probe)
    if abs(duration - 15.0) > 0.25:
        raise SystemExit(f"Final film duration is {duration:.3f}s, expected 15s")

    print(final)


if __name__ == "__main__":
    main()
