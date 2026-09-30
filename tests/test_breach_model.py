"""
Tests for simulation/breach_model.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from simulation.breach_model import (
    peak_discharge_m3s,
    flooded_area_km2_estimate,
    warning_level,
    time_to_peak_s,
)


class TestPeakDischarge:
    def test_zero_width_returns_zero(self):
        assert peak_discharge_m3s(0, 10) == 0.0

    def test_zero_head_returns_zero(self):
        assert peak_discharge_m3s(30, 0) == 0.0

    def test_positive_for_valid_inputs(self):
        q = peak_discharge_m3s(30, 15)
        assert q > 0

    def test_larger_width_gives_larger_discharge(self):
        q_small = peak_discharge_m3s(10, 10)
        q_large = peak_discharge_m3s(60, 10)
        assert q_large > q_small

    def test_larger_head_gives_larger_discharge(self):
        q_low  = peak_discharge_m3s(30, 5)
        q_high = peak_discharge_m3s(30, 20)
        assert q_high > q_low

    def test_severe_breach_realistic_order_of_magnitude(self):
        """Severe breach should produce tens of thousands of m³/s (illustrative)."""
        q = peak_discharge_m3s(60, 25)
        assert 1_000 < q < 1_000_000, f"Unexpected severe discharge: {q}"


class TestFloodedArea:
    def test_returns_positive(self):
        area = flooded_area_km2_estimate(30, 15, 60)
        assert area > 0

    def test_larger_breach_gives_larger_area(self):
        small = flooded_area_km2_estimate(10, 5, 30)
        large = flooded_area_km2_estimate(60, 25, 90)
        assert large > small


class TestWarningLevel:
    @pytest.mark.parametrize("depth, expected", [
        (0.0,  "Low"),
        (0.3,  "Low"),
        (0.5,  "Moderate"),
        (1.5,  "Moderate"),
        (2.0,  "High"),
        (4.9,  "High"),
        (5.0,  "Critical"),
        (12.0, "Critical"),
    ])
    def test_levels(self, depth, expected):
        assert warning_level(depth) == expected


class TestTimeToPeak:
    def test_scales_with_formation_time(self):
        assert time_to_peak_s(10) == pytest.approx(600.0)
        assert time_to_peak_s(20) == pytest.approx(1200.0)
