"""Simulation result data model — matches docs/API_AND_DATA_CONTRACTS.md."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid


class SimulationStatus(str, Enum):
    CREATED = "created"
    VALIDATED = "validated"
    PREPARING = "preparing"
    RUNNING = "running"
    POST_PROCESSING = "post_processing"
    COMPLETED = "completed"
    FAILED = "failed"

    def label(self) -> str:
        return self.value.replace("_", " ").title()

    def is_terminal(self) -> bool:
        return self in (SimulationStatus.COMPLETED, SimulationStatus.FAILED)

    def progress_pct(self) -> int:
        """Approximate UI progress bar value (0–100)."""
        order = {
            SimulationStatus.CREATED: 5,
            SimulationStatus.VALIDATED: 15,
            SimulationStatus.PREPARING: 30,
            SimulationStatus.RUNNING: 70,
            SimulationStatus.POST_PROCESSING: 90,
            SimulationStatus.COMPLETED: 100,
            SimulationStatus.FAILED: 0,
        }
        return order.get(self, 0)


@dataclass
class SimulationResult:
    """
    Output contract for a completed (or in-progress) simulation.

    None values indicate that a metric has NOT yet been calculated.
    Per spec: never substitute fake values for None.
    All numeric values here come from the mock or ANUGA runner.
    """
    simulation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scenario_id: Optional[str] = None
    scenario_name: Optional[str] = None
    status: SimulationStatus = SimulationStatus.CREATED
    status_message: str = ""

    # Output metrics — None until computed
    duration_min: Optional[float] = None
    max_water_depth_m: Optional[float] = None
    max_velocity_mps: Optional[float] = None
    flooded_area_km2: Optional[float] = None
    affected_settlements: Optional[int] = None
    affected_roads_km: Optional[float] = None
    peak_discharge_m3s: Optional[float] = None
    warning_level: Optional[str] = None  # Low / Moderate / High / Critical

    # Output file paths
    depth_layer: Optional[str] = None
    extent_layer: Optional[str] = None
    velocity_layer: Optional[str] = None
    risk_layer: Optional[str] = None

    # GeoJSON payloads (in-memory for prototype)
    flood_extent_geojson: Optional[dict] = None
    risk_zones_geojson: Optional[dict] = None
    settlements_geojson: Optional[dict] = None
    roads_geojson: Optional[dict] = None

    # Time-series data for timeline playback
    time_steps: Optional[list[float]] = None           # minutes
    depth_at_steps: Optional[list[float]] = None       # max depth m at each step
    area_at_steps: Optional[list[float]] = None        # flooded area km² at each step

    # Source label — always shown in UI
    data_source_label: str = "⚠️ DEMO DATA — Not real ANUGA output"
    is_mock: bool = True

    def to_dict(self) -> dict:
        return {
            "simulation_id": self.simulation_id,
            "scenario_id": self.scenario_id,
            "status": self.status.value,
            "duration_min": self.duration_min,
            "max_water_depth_m": self.max_water_depth_m,
            "max_velocity_mps": self.max_velocity_mps,
            "flooded_area_km2": self.flooded_area_km2,
            "affected_settlements": self.affected_settlements,
            "affected_roads_km": self.affected_roads_km,
            "warning_level": self.warning_level,
            "depth_layer": self.depth_layer,
            "extent_layer": self.extent_layer,
            "velocity_layer": self.velocity_layer,
            "risk_layer": self.risk_layer,
            "is_mock": self.is_mock,
        }
