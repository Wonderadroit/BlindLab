# BlindLab

BlindLab is an evidence-driven laboratory for window-blind experiments.

## Current milestone: v0.3 — photorealistic visual validation

The experiment loop now has three layers:

1. **Optimization model:** solar position -> objective -> angle sweep -> best angle.
2. **Geometry validation:** the selected blind configuration is represented as finite slat planes and tested against a sun ray.
3. **Visual validation:** the same selected angle is rendered inside a composed room scene with Blender so the result can be inspected as an image.

The important design rule is:

> The renderer is evidence about the rendered scene, not proof of calibrated physical reality.

The v0.3 renderer uses a presentation-oriented architectural scene: room surfaces, window glass, furniture, Venetian slats, directional sunlight, fill light, and a composed camera. This makes the result useful for demonstrations and visual exploration while keeping scientific claims conservative.

### Experiment boundary

The current optimizer and renderer do **not** claim calibrated lux, glare index, solar heat gain, thermal comfort, or exact material/glass optical behavior. Those require measurement and calibration.

### Commands

    pytest -q
    python -m blindlab --output artifacts/experiment.json

If Blender is installed:

    ANGLE=45
    blender -b --python blender/scene_v03.py -- --angle "$ANGLE" --output artifacts/blindlab_v03.png

### Evidence ladder

mathematical prediction -> geometric proxy -> rendered visual evidence -> measured calibration

BlindLab should only promote a result to a stronger claim when the next evidence layer actually validates it.
