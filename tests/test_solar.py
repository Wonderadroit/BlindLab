from datetime import datetime, timezone
import pytest
from blindlab.solar import position

def test_invalid_latitude_rejected():
    with pytest.raises(ValueError):
        position(datetime.now(timezone.utc),91,0,0)

def test_lagos_midday_is_daylight():
    sun=position(datetime(2026,10,4,11,0,tzinfo=timezone.utc),6.5244,3.3792,1)
    assert sun.daylight and sun.altitude_deg > 0

def test_azimuth_is_normalized():
    sun=position(datetime(2026,10,4,11,0,tzinfo=timezone.utc),6.5244,3.3792,1)
    assert 0 <= sun.azimuth_deg < 360
