from blindlab.model import Blind, ExperimentWeights, Window
from blindlab.optimizer import choose_best, score_candidate, sweep_angles
from blindlab.solar import SunPosition
import pytest

def test_sweep_has_expected_candidates():
    candidates=sweep_angles(Window(180),SunPosition(50,180,True),ExperimentWeights(),0,90,5)
    assert len(candidates)==19 and candidates[0].angle_deg==0 and candidates[-1].angle_deg==90

def test_best_is_deterministic():
    candidates=sweep_angles(Window(180),SunPosition(50,180,True),ExperimentWeights())
    assert choose_best(candidates)==choose_best(candidates)

def test_night_has_no_heat_penalty():
    c=score_candidate(Blind(45),Window(180),SunPosition(-5,180,False),ExperimentWeights())
    assert c.heat==0 and c.daylight==1

def test_empty_candidates_rejected():
    with pytest.raises(ValueError): choose_best([])
