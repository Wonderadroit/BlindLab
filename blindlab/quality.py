"""Machine-checkable quality gates for BlindLab's photorealistic production blueprint.

These checks validate production intent and continuity. They do not claim generated
pixels are physically real; visual acceptance remains a human review gate.
"""

from .creative import FIRST_FILM, REALISM_RULES, Shot, production_prompt


def validate_production_blueprint(shots: tuple[Shot, ...] = FIRST_FILM) -> list[str]:
    """Return blocking issues; an empty list means the blueprint is internally coherent."""
    issues: list[str] = []

    if not shots:
        return ["no shots defined"]

    ids = [shot.id for shot in shots]
    if ids != [f"{i:02d}" for i in range(1, len(shots) + 1)]:
        issues.append("shot ids must be sequential two-digit identifiers")
    if len(set(ids)) != len(ids):
        issues.append("shot ids must be unique")

    if any(shot.duration_s <= 0 for shot in shots):
        issues.append("all shots must have positive durations")
    if sum(shot.duration_s for shot in shots) != 15.0:
        issues.append("first film must total exactly 15 seconds")

    if len(shots) >= 4:
        narrative_locations = [shot.location for shot in shots[:4]]
        if narrative_locations[1:] != ["same location", "same location", "same location, wider view"]:
            issues.append("shots 02-04 must preserve location continuity")

    required_rules = {
        "photographic human anatomy and skin texture",
        "physically plausible lighting and reflections",
        "natural lens depth of field and motion blur",
        "real materials with small imperfections",
        "no 3D-rendered or videogame appearance",
    }
    if not required_rules.issubset(set(REALISM_RULES)):
        issues.append("core photorealism rules are incomplete")

    for shot in shots:
        if not shot.realism_checks:
            issues.append(f"shot {shot.id} has no realism checks")
        prompt = production_prompt(shot)
        if "Photorealistic cinematic frame" not in prompt:
            issues.append(f"shot {shot.id} prompt is missing photorealistic framing")
        if "Do not make it look like CGI" not in prompt:
            issues.append(f"shot {shot.id} prompt is missing anti-CGI direction")

    return issues


def assert_production_blueprint(shots: tuple[Shot, ...] = FIRST_FILM) -> None:
    issues = validate_production_blueprint(shots)
    if issues:
        raise AssertionError("; ".join(issues))
