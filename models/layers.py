"""Layer descriptor dataclasses for GIS outputs."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class FloodExtentLayer:
    """GeoJSON-based flood extent polygon."""
    geojson: dict
    crs: str = "EPSG:4326"
    source: str = "mock"
    description: str = "Flood inundation extent (demo)"


@dataclass
class RiskZoneLayer:
    """Risk zone classification layer."""
    geojson: dict                 # FeatureCollection with risk_level property
    crs: str = "EPSG:4326"
    classification: dict = None   # threshold dict used to derive zones

    def __post_init__(self):
        if self.classification is None:
            self.classification = {
                "Low": (0.0, 0.5),
                "Moderate": (0.5, 2.0),
                "High": (2.0, 5.0),
                "Critical": (5.0, float("inf")),
            }


@dataclass
class SettlementLayer:
    """Point layer of settlements / populated places."""
    geojson: dict
    crs: str = "EPSG:4326"
    count: int = 0
    affected_count: Optional[int] = None


@dataclass
class RoadLayer:
    """Line layer of roads."""
    geojson: dict
    crs: str = "EPSG:4326"
    total_length_km: Optional[float] = None
    affected_length_km: Optional[float] = None
