
"""Scenario data model — matches docs/API_AND_DATA_CONTRACTS.md."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class DamConfig:
    """Static configuration for a dam in the study area."""
    dam_id: str
    name: str
    latitude: float
    longitude: float
    height_m: float
    storage_mcm: float  # Million Cubic Metres
    river: str
    location_description: str


# ---------------------------------------------------------------------------
# Pre-configured demo dam — Hirakud Dam, Odisha, India
# ---------------------------------------------------------------------------
HIRAKUD_DAM = DamConfig(
    dam_id="hirakud-demo",
    name="Hirakud Dam (Demo)",
    latitude=21.525,
    longitude=83.873,
    height_m=60.96,
    storage_mcm=8141.0,
    river="Mahanadi River",
    location_description="Sambalpur, Odisha, India",
)

AVAILABLE_DAMS: dict[str, DamConfig] = {
    HIRAKUD_DAM.dam_id: HIRAKUD_DAM,
}


@dataclass
class Scenario:
    """
    Complete input specification for one dam-break simulation run.

    All physical units are SI (metres, minutes) unless noted.
    Matches the data contract in docs/API_AND_DATA_CONTRACTS.md.
    """
    dam_id: str
    breach_width_m: float
    breach_depth_m: float
    formation_time_min: float
    duration_min: float
    reservoir_level_m: float = 60.0
    scenario_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    preset_name: Optional[str] = None

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------
    def validate(self) -> list[str]:
        """Return a list of validation error messages (empty = valid)."""
        errors: list[str] = []

        dam = AVAILABLE_DAMS.get(self.dam_id)
        if dam is None:
            errors.append(f"Unknown dam_id '{self.dam_id}'.")

        if self.breach_width_m <= 0:
            errors.append("Breach width must be positive.")
        if self.breach_width_m > 500:
            errors.append("Breach width > 500 m is physically unreasonable for a demo dam.")

        if self.breach_depth_m <= 0:
            errors.append("Breach depth must be positive.")
        if dam and self.breach_depth_m > dam.height_m:
            errors.append(
                f"Breach depth ({self.breach_depth_m} m) exceeds dam height "
                f"({dam.height_m} m)."
            )

        if self.formation_time_min <= 0:
            errors.append("Breach formation time must be positive.")

        if self.duration_min <= 0:
            errors.append("Simulation duration must be positive.")
        if self.duration_min > 720:
            errors.append("Simulation duration > 720 minutes is not supported in this prototype.")

        if self.reservoir_level_m <= 0:
            errors.append("Reservoir level must be positive.")
        if dam and self.reservoir_level_m > dam.height_m:
            errors.append(
                f"Reservoir level ({self.reservoir_level_m} m) exceeds dam height "
                f"({dam.height_m} m)."
            )

        return errors

    @property
    def is_valid(self) -> bool:
        return len(self.validate()) == 0

    def to_dict(self) -> dict:
        return {
            "scenario_id": self.scenario_id,
            "dam_id": self.dam_id,
            "preset_name": self.preset_name,
            "breach_width_m": self.breach_width_m,
            "breach_depth_m": self.breach_depth_m,
            "formation_time_min": self.formation_time_min,
            "duration_min": self.duration_min,
            "reservoir_level_m": self.reservoir_level_m,
        }
