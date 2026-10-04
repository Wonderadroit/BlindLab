from blindlab.creative import FIRST_FILM
from blindlab.quality import assert_production_blueprint, validate_production_blueprint


def test_first_film_passes_quality_gate():
    assert validate_production_blueprint(FIRST_FILM) == []
    assert_production_blueprint(FIRST_FILM)


def test_quality_gate_rejects_duplicate_ids():
    broken = (FIRST_FILM[0], FIRST_FILM[0])
    issues = validate_production_blueprint(broken)
    assert "shot ids must be sequential two-digit identifiers" in issues
    assert "shot ids must be unique" in issues


def test_quality_gate_rejects_wrong_duration():
    broken = tuple(FIRST_FILM[:4]) + (FIRST_FILM[4].__class__(
        "05", 3.0, FIRST_FILM[4].location, FIRST_FILM[4].action,
        FIRST_FILM[4].camera, FIRST_FILM[4].lighting, FIRST_FILM[4].realism_checks
    ),)
    assert "first film must total exactly 15 seconds" in validate_production_blueprint(broken)
