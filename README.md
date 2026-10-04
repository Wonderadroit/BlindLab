# BlindLab

BlindLab is an evidence-driven laboratory for window-blind experiments.

## Current milestone: v0.2

The experiment loop now has two layers:

1. **Optimization model:** solar position → objective → angle sweep → best angle.
2. **Geometry validation:** the selected blind configuration is represented as finite slat planes and tested against a sun ray.

A Blender scene generator mirrors the conceptual slat stack so the mathematical model and visual scene share the same angle/count/window assumptions.

### Important boundary

The v0.2 geometry test is still a validation proxy, **not a calibrated lighting simulation**. It does not claim real lux, glare, heat transfer, glass optics, or material behavior.

### Commands

```bash
pytest -q
python -m blindlab
```

For Blender:

```bash
blender -b --python blender/scene_v02.py -- --angle 45 --output /tmp/blindlab_v02.blend
```

CI proves deterministic software behavior. Physical accuracy will require calibration against measured light/temperature data before customer-facing claims.
