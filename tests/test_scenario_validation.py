"""
Tests for scenario validation (models/scenario.py).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from models.scenario import Scenario, HIRAKUD_DAM


VALID_KWARGS = dict(
    dam_id="hirakud-demo",
    breach_width_m=30.0,
    breach_depth_m=15.0,
    formation_time_min=10.0,
    duration_min=60.0,
    reservoir_level_m=55.0,
)


class TestScenarioValidation:

    def test_valid_scenario_has_no_errors(self):
        s = Scenario(**VALID_KWARGS)
        assert s.validate() == []
        assert s.is_valid

    def test_invalid_dam_id(self):
        s = Scenario(**{**VALID_KWARGS, "dam_id": "nonexistent"})
        errors = s.validate()
        assert any("dam_id" in e for e in errors)

    def test_zero_breach_width(self):
        s = Scenario(**{**VALID_KWARGS, "breach_width_m": 0})
        assert any("width" in e.lower() for e in s.validate())

    def test_negative_breach_width(self):
        s = Scenario(**{**VALID_KWARGS, "breach_width_m": -5})
        assert any("width" in e.lower() for e in s.validate())

    def test_breach_width_too_large(self):
        s = Scenario(**{**VALID_KWARGS, "breach_width_m": 600})
        errors = s.validate()
        assert any("width" in e.lower() or "unreasonable" in e.lower() for e in errors)

    def test_breach_depth_exceeds_dam_height(self):
        s = Scenario(**{**VALID_KWARGS, "breach_depth_m": HIRAKUD_DAM.height_m + 1})
        errors = s.validate()
        assert any("depth" in e.lower() and "height" in e.lower() for e in errors)

    def test_reservoir_level_exceeds_dam_height(self):
        s = Scenario(**{**VALID_KWARGS, "reservoir_level_m": HIRAKUD_DAM.height_m + 5})
        errors = s.validate()
        assert any("level" in e.lower() and "height" in e.lower() for e in errors)

    def test_zero_duration(self):
        s = Scenario(**{**VALID_KWARGS, "duration_min": 0})
        assert any("duration" in e.lower() for e in s.validate())

    def test_duration_too_large(self):
        s = Scenario(**{**VALID_KWARGS, "duration_min": 800})
        assert any("720" in e or "duration" in e.lower() for e in s.validate())

    def test_zero_formation_time(self):
        s = Scenario(**{**VALID_KWARGS, "formation_time_min": 0})
        assert any("formation" in e.lower() for e in s.validate())

    def test_preset_name_stored(self):
        s = Scenario(**{**VALID_KWARGS, "preset_name": "Severe"})
        assert s.preset_name == "Severe"

    def test_scenario_to_dict_has_required_keys(self):
        s = Scenario(**VALID_KWARGS)
        d = s.to_dict()
        for key in ("scenario_id", "dam_id", "breach_width_m", "breach_depth_m",
                    "formation_time_min", "duration_min"):
            assert key in d, f"Missing key: {key}"
