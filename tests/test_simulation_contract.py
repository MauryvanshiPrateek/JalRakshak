"""
Tests for simulation output data contract (mock runner + simulation service).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from models.scenario import Scenario
from models.simulation_result import SimulationResult, SimulationStatus
from simulation.simulation_service import SimulationService


MEDIUM_SCENARIO = Scenario(
    dam_id="hirakud-demo",
    breach_width_m=30.0,
    breach_depth_m=15.0,
    formation_time_min=10.0,
    duration_min=60.0,
    reservoir_level_m=55.0,
    preset_name="Medium",
)


@pytest.fixture(scope="module")
def completed_result() -> SimulationResult:
    """Run a full mock simulation once and share the result."""
    service = SimulationService()
    result = service.submit(MEDIUM_SCENARIO, blocking=True)
    return result


class TestSimulationContract:

    def test_status_is_completed(self, completed_result):
        assert completed_result.status == SimulationStatus.COMPLETED

    def test_simulation_id_present(self, completed_result):
        assert completed_result.simulation_id

    def test_flooded_area_not_none(self, completed_result):
        assert completed_result.flooded_area_km2 is not None

    def test_flooded_area_positive(self, completed_result):
        assert completed_result.flooded_area_km2 > 0

    def test_max_depth_not_none(self, completed_result):
        assert completed_result.max_water_depth_m is not None

    def test_max_depth_positive(self, completed_result):
        assert completed_result.max_water_depth_m > 0

    def test_max_velocity_positive(self, completed_result):
        assert completed_result.max_velocity_mps > 0

    def test_warning_level_valid(self, completed_result):
        assert completed_result.warning_level in ("Low", "Moderate", "High", "Critical")

    def test_flood_extent_geojson_present(self, completed_result):
        gj = completed_result.flood_extent_geojson
        assert gj is not None
        assert gj.get("type") == "FeatureCollection"
        assert len(gj.get("features", [])) > 0

    def test_settlements_geojson_present(self, completed_result):
        gj = completed_result.settlements_geojson
        assert gj is not None
        assert gj.get("type") == "FeatureCollection"

    def test_is_mock_flagged(self, completed_result):
        assert completed_result.is_mock is True

    def test_data_source_label_warns_demo(self, completed_result):
        assert "DEMO" in completed_result.data_source_label.upper()

    def test_time_steps_list(self, completed_result):
        assert isinstance(completed_result.time_steps, list)
        assert len(completed_result.time_steps) > 1

    def test_depth_at_steps_matches_time_steps(self, completed_result):
        assert len(completed_result.depth_at_steps) == len(completed_result.time_steps)

    def test_area_at_steps_matches_time_steps(self, completed_result):
        assert len(completed_result.area_at_steps) == len(completed_result.time_steps)

    def test_to_dict_has_contract_keys(self, completed_result):
        d = completed_result.to_dict()
        for key in ("simulation_id", "status", "flooded_area_km2",
                    "max_water_depth_m", "max_velocity_mps", "warning_level"):
            assert key in d, f"Missing contract key: {key}"

    def test_failed_on_invalid_scenario(self):
        service = SimulationService()
        bad = Scenario(
            dam_id="hirakud-demo",
            breach_width_m=-10,    # invalid
            breach_depth_m=15,
            formation_time_min=10,
            duration_min=60,
        )
        result = service.submit(bad, blocking=True)
        assert result.status == SimulationStatus.FAILED
