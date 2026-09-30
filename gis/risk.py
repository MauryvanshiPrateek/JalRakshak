"""
Risk classification and exposure analysis for JalRakshak.

Classifies flood risk for settlements and roads based on water depth
and spatial intersection with the flood extent polygon.

⚠️  DEMO DATA — spatial intersection uses simplified bounding-box logic
rather than proper GIS polygon-point intersection, because GeoPandas
is an optional heavy dependency for the prototype UI.  Replace with
proper geopandas intersection when available.
"""
from __future__ import annotations
import copy
import math


# ---------------------------------------------------------------------------
# Risk thresholds (depth in metres)
# ---------------------------------------------------------------------------
RISK_THRESHOLDS = {
    "Low":      (0.0,   0.5),
    "Moderate": (0.5,   2.0),
    "High":     (2.0,   5.0),
    "Critical": (5.0,   float("inf")),
}

RISK_COLORS = {
    "Low":      "#22c55e",   # green
    "Moderate": "#eab308",   # yellow
    "High":     "#f97316",   # orange
    "Critical": "#ef4444",   # red
    "None":     "#94a3b8",   # slate (not flooded)
}


def classify_depth(depth_m: float) -> str:
    """Return risk level label for a given water depth."""
    for level, (lo, hi) in RISK_THRESHOLDS.items():
        if lo <= depth_m < hi:
            return level
    return "Low"


def estimate_depth_at_point(
    lon: float,
    lat: float,
    flood_extent_geojson: dict,
    max_depth_m: float,
    dam_lon: float = 83.873,
    dam_lat: float = 21.525,
) -> float:
    """
    Estimate water depth at a point using distance-decay from the dam.

    This is a geometric approximation for demo purposes only.
    Real depth values come from ANUGA raster outputs.
    """
    if not _point_in_flood(lon, lat, flood_extent_geojson):
        return 0.0

    # Depth decays with distance from dam
    dist = math.sqrt((lon - dam_lon) ** 2 + (lat - dam_lat) ** 2)
    max_dist = 0.80  # degrees — rough extent of severe scenario
    decay = max(0.0, 1.0 - (dist / max_dist) ** 0.7)
    return round(max_depth_m * decay, 2)


def apply_risk_to_settlements(
    settlements_geojson: dict,
    flood_extent_geojson: dict,
    max_depth_m: float,
) -> dict:
    """
    Mark settlements as affected and assign risk levels.

    Returns a new GeoJSON FeatureCollection (original is not mutated).
    """
    result = copy.deepcopy(settlements_geojson)
    for feature in result["features"]:
        lon, lat = feature["geometry"]["coordinates"]
        depth = estimate_depth_at_point(lon, lat, flood_extent_geojson, max_depth_m)
        feature["properties"]["flood_depth_m"] = depth
        feature["properties"]["affected"] = depth > 0.1
        feature["properties"]["risk_level"] = classify_depth(depth) if depth > 0.1 else "None"
    return result


def apply_risk_to_roads(
    roads_geojson: dict,
    flood_extent_geojson: dict,
    max_depth_m: float,
) -> dict:
    """
    Mark road segments as affected based on midpoint intersection.
    """
    result = copy.deepcopy(roads_geojson)
    for feature in result["features"]:
        coords = feature["geometry"]["coordinates"]
        # Check midpoint of road
        mid_idx = len(coords) // 2
        lon, lat = coords[mid_idx]
        depth = estimate_depth_at_point(lon, lat, flood_extent_geojson, max_depth_m)
        feature["properties"]["flood_depth_m"] = depth
        feature["properties"]["affected"] = depth > 0.1
        feature["properties"]["risk_level"] = classify_depth(depth) if depth > 0.1 else "None"
    return result


def compute_exposure_summary(
    settlements_geojson: dict,
    roads_geojson: dict,
) -> dict:
    """Aggregate exposure statistics from risk-annotated layers."""
    settlements = settlements_geojson.get("features", [])
    roads = roads_geojson.get("features", [])

    affected_settlements = [f for f in settlements if f["properties"].get("affected")]
    affected_roads = [f for f in roads if f["properties"].get("affected")]

    population_at_risk = sum(
        f["properties"].get("population_approx", 0) for f in affected_settlements
    )
    risk_counts = {"Low": 0, "Moderate": 0, "High": 0, "Critical": 0}
    for f in affected_settlements:
        lvl = f["properties"].get("risk_level", "Low")
        if lvl in risk_counts:
            risk_counts[lvl] += 1

    return {
        "total_settlements": len(settlements),
        "affected_settlements": len(affected_settlements),
        "population_at_risk_approx": population_at_risk,
        "total_roads_checked": len(roads),
        "affected_roads": len(affected_roads),
        "risk_counts": risk_counts,
    }


def build_risk_zones_geojson(flood_extent_geojson: dict, max_depth_m: float) -> dict:
    """
    Build risk zone sub-polygons by splitting the flood extent into
    concentric bands (Critical → High → Moderate → Low) from the dam
    outward.

    This is a geometric simplification for map display only.
    """
    features = []
    bands = [
        ("Critical", 0.0,  0.25, "#ef4444", 0.55),
        ("High",     0.25, 0.50, "#f97316", 0.40),
        ("Moderate", 0.50, 0.75, "#eab308", 0.35),
        ("Low",      0.75, 1.00, "#22c55e", 0.25),
    ]
    for label, t_start, t_end, color, _ in bands:
        # Only show zones where depth supports that level
        min_depth, _ = RISK_THRESHOLDS[label]
        if max_depth_m < min_depth:
            continue
        poly = _risk_band_polygon(t_start, t_end)
        features.append({
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [poly]},
            "properties": {
                "risk_level": label,
                "color": color,
                "description": f"{label} Risk Zone",
            },
        })
    return {"type": "FeatureCollection", "features": features}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
DAM_LON = 83.873
DAM_LAT = 21.525
MAX_REACH_LON = 0.80
MAX_HALF_WIDTH = 0.040


def _point_in_flood(lon: float, lat: float, flood_geojson: dict) -> bool:
    """
    Approximate point-in-polygon check using the flood extent bounding box.
    Good enough for demo risk classification; replace with Shapely for accuracy.
    """
    for feature in flood_geojson.get("features", []):
        coords = feature["geometry"].get("coordinates", [[]])[0]
        if not coords:
            continue
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        if min(lons) <= lon <= max(lons) and min(lats) <= lat <= max(lats):
            return True
    return False


def _risk_band_polygon(t_start: float, t_end: float) -> list[list[float]]:
    """Build a flood corridor polygon for a given downstream fraction range."""
    import math
    n = 16
    upper = []
    lower = []
    for i in range(n + 1):
        t = t_start + (t_end - t_start) * i / n
        lon = DAM_LON + MAX_REACH_LON * t
        lat = DAM_LAT - 0.18 * t
        w = MAX_HALF_WIDTH * math.sqrt(t + 0.05)
        upper.append([round(lon, 5), round(lat + w, 5)])
        lower.insert(0, [round(lon, 5), round(lat - w, 5)])
    ring = upper + lower
    ring.append(ring[0])
    return ring
