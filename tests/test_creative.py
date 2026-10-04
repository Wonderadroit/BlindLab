from blindlab.creative import FIRST_FILM, REALISM_RULES, production_prompt


def test_first_film_is_15_seconds():
    assert len(FIRST_FILM) == 5
    assert sum(s.duration_s for s in FIRST_FILM) == 15.0


def test_realism_rules_are_present():
    assert "no 3D-rendered or videogame appearance" in REALISM_RULES
    for shot in FIRST_FILM:
        assert shot.realism_checks
        assert "Photorealistic" in production_prompt(shot)
