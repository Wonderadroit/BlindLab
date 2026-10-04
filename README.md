# BlindLab

BlindLab is an evidence-driven laboratory for window-blind experiments.

## v0.1

The first real loop is:

`solar position → blind model → angle sweep → objective score → evidence artifact`

This version is deliberately **not** a photorealistic lighting or thermal simulator. Its geometry model is an explicit, inspectable proxy. That gives us a deterministic foundation that can later be replaced by ray tracing, calibrated measurements, or hardware without rewriting the experiment contract.

### Run

```bash
python -m pip install -e .
pytest -q
python -m blindlab
```

The CLI writes `artifacts/experiment.json`.

### Blender

`blender/scene_v01.py` creates a simple room/window/Venetian-blind scene with 24 adjustable slats and a sun light. CI intentionally does not require Blender; rendering is a later visual-validation layer.

### Evidence rules

Every experiment records inputs, assumptions, candidates, the selected configuration, and limitations. A green test is not treated as proof of physical accuracy.
