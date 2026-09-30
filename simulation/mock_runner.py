"""
Mock Simulation Runner — Phase 1 UI development.

Implements the same interface as AnugaSimulationEngine but returns
clearly-labelled synthetic/illustrative results without running ANUGA.

⚠️  ALL OUTPUTS ARE MOCK DATA — not real hydrodynamic simulation results.
Replace MockSimulationEngine with AnugaSimulationEngine (Phase 4+) to use
real ANUGA outputs.  The UI and SimulationService do not need to change.
"""
from __future__ import annotations
import time
import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.scenario import Scenario, AVAILABLE_DAMS
from models.simulation_result import SimulationResult, SimulationStatus
from simulation.breach_model import (
    peak_discharge_m3s,
    flooded_area_km2_estimate,
    warning_level,
)
from gis.flood_extent import flood_extent_geojson, flood_metrics, time_series
from gis.vector import get_settlements_geojson, get_roads_geojson
from gis.risk import (
    apply_risk_to_settlements,
    apply_risk_to_roads,
    compute_exposure_summary,
    build_risk_zones_geojson,
)


class MockSimulationEngine:
    """
    Simulates a dam-break scenario using illustrative geometric/analytical
    calculations.  Designed to exercise the full UI pipeline without ANUGA.

    Progress is reported via a callback: callback(status, message, pct).
    """

    def run(
        self,
        scenario: Scenario,
        result: SimulationResult,
        progress_callback=None,
    ) -> SimulationResult:
        """
        Execute the mock simulation lifecycle.

        Parameters
        ----------
        scenario : Scenario
        result : SimulationResult
            Pre-created result object to update in place.
        progress_callback : callable(status, message, pct) | None

        Returns
        -------
        SimulationResult with all mock fields populated.
        """
        def _progress(status: SimulationStatus, msg: str):
            result.status = status
            result.status_message = msg
            if progress_callback:
                progress_callback(status, msg, status.progress_pct())

        # ── VALIDATED ──────────────────────────────────────────────────────
        _progress(SimulationStatus.VALIDATED, "Scenario validated. Parameters accepted.")
        time.sleep(0.4)

        # ── PREPARING ──────────────────────────────────────────────────────
        _progress(SimulationStatus.PREPARING, "Preparing computational domain and terrain…")
        time.sleep(0.8)

        # ── RUNNING ────────────────────────────────────────────────────────
        _progress(SimulationStatus.RUNNING, "Running illustrative dam-break calculation…")
        time.sleep(1.2)

        # Core calculations (illustrative formulae — see breach_model.py)
        dam = AVAILABLE_DAMS.get(scenario.dam_id)
        head = min(scenario.reservoir_level_m, scenario.breach_depth_m)
        q_peak = peak_discharge_m3s(scenario.breach_width_m, head)

        metrics = flood_metrics(scenario.breach_width_m, scenario.breach_depth_m)
        max_depth = metrics["max_water_depth_m"]
        max_vel = metrics["max_velocity_mps"]
        area_km2 = metrics["flooded_area_km2"]

        time.sleep(0.5)

        # ── POST-PROCESSING ─────────────────────────────────────────────────
        _progress(SimulationStatus.POST_PROCESSING, "Converting outputs to GIS layers…")
        time.sleep(0.6)

        # Generate GeoJSON layers
        extent_gj = flood_extent_geojson(
            scenario.breach_width_m,
            scenario.breach_depth_m,
            scenario.duration_min,
            time_fraction=1.0,
        )
        risk_gj = build_risk_zones_geojson(extent_gj, max_depth)

        # Apply risk to settlements and roads
        settlements_raw = get_settlements_geojson()
        roads_raw = get_roads_geojson()

        settlements_risk = apply_risk_to_settlements(settlements_raw, extent_gj, max_depth)
        roads_risk = apply_risk_to_roads(roads_raw, extent_gj, max_depth)

        exposure = compute_exposure_summary(settlements_risk, roads_risk)

        # Time series for playback
        t_steps, d_steps, a_steps = time_series(
            scenario.breach_width_m,
            scenario.breach_depth_m,
            scenario.duration_min,
        )

        time.sleep(0.4)

        # ── COMPLETED ────────────────────────────────────────────────────────
        _progress(SimulationStatus.COMPLETED, "Simulation complete. Results ready.")

        # Populate result
        result.duration_min = scenario.duration_min
        result.max_water_depth_m = max_depth
        result.max_velocity_mps = max_vel
        result.flooded_area_km2 = area_km2
        result.peak_discharge_m3s = round(q_peak, 1)
        result.affected_settlements = exposure["affected_settlements"]
        result.affected_roads_km = None   # not calculated in mock
        result.warning_level = warning_level(max_depth)
        result.flood_extent_geojson = extent_gj
        result.risk_zones_geojson = risk_gj
        result.settlements_geojson = settlements_risk
        result.roads_geojson = roads_risk
        result.time_steps = t_steps
        result.depth_at_steps = d_steps
        result.area_at_steps = a_steps
        result.scenario_name = scenario.preset_name or "Custom"
        result.scenario_id = scenario.scenario_id
        result.is_mock = True
        result.data_source_label = "⚠️ DEMO DATA — Illustrative calculation, not real ANUGA output"

        return result


def create_instant_demo_result(scenario: Scenario | None = None) -> SimulationResult:
    """
    Instantly create a fully completed SimulationResult for UI preview and landing map,
    without any artificial time.sleep delays.
    """
    if scenario is None:
        scenario = Scenario(
            dam_id="hirakud-demo",
            breach_width_m=45.0,
            breach_depth_m=28.0,
            formation_time_min=72.0,
            duration_min=360.0,
            reservoir_level_m=58.0,
            preset_name="Hirakud Severe Breach Scenario",
        )

    result = SimulationResult(scenario_id="instant_demo")
    head = min(scenario.reservoir_level_m, scenario.breach_depth_m)
    q_peak = peak_discharge_m3s(scenario.breach_width_m, head)

    metrics = flood_metrics(scenario.breach_width_m, scenario.breach_depth_m)
    max_depth = metrics["max_water_depth_m"]
    max_vel = metrics["max_velocity_mps"]
    area_km2 = metrics["flooded_area_km2"]

    extent_gj = flood_extent_geojson(
        scenario.breach_width_m,
        scenario.breach_depth_m,
        scenario.duration_min,
        time_fraction=1.0,
    )
    risk_gj = build_risk_zones_geojson(extent_gj, max_depth)

    settlements_raw = get_settlements_geojson()
    roads_raw = get_roads_geojson()

    settlements_risk = apply_risk_to_settlements(settlements_raw, extent_gj, max_depth)
    roads_risk = apply_risk_to_roads(roads_raw, extent_gj, max_depth)
    exposure = compute_exposure_summary(settlements_risk, roads_risk)

    t_steps, d_steps, a_steps = time_series(
        scenario.breach_width_m,
        scenario.breach_depth_m,
        scenario.duration_min,
    )

    result.status = SimulationStatus.COMPLETED
    result.status_message = "Simulation complete. Results ready."
    result.duration_min = scenario.duration_min
    result.max_water_depth_m = max_depth
    result.max_velocity_mps = max_vel
    result.flooded_area_km2 = area_km2
    result.peak_discharge_m3s = round(q_peak, 1)
    result.affected_settlements = exposure["affected_settlements"]
    result.affected_roads_km = None
    result.warning_level = warning_level(max_depth)
    result.flood_extent_geojson = extent_gj
    result.risk_zones_geojson = risk_gj
    result.settlements_geojson = settlements_risk
    result.roads_geojson = roads_risk
    result.time_steps = t_steps
    result.depth_at_steps = d_steps
    result.area_at_steps = a_steps
    result.scenario_name = scenario.preset_name or "Custom"
    result.scenario_id = scenario.scenario_id
    result.is_mock = True
    result.data_source_label = "⚠️ DEMO DATA — Illustrative calculation, not real ANUGA output"

    return result

