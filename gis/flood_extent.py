"""
Flood extent generation for the JalRakshak demo.

Generates mock flood-extent GeoJSON polygons that expand downstream
along the Mahanadi River corridor based on breach severity.

⚠️  DEMO DATA — these extents are geometric approximations for UI
demonstration purposes only.  They are not ANUGA simulation outputs.
"""
from __future__ import annotations
import math


# ---------------------------------------------------------------------------
# Dam / river geometry (from gis.domain)
# ---------------------------------------------------------------------------
DAM_LON = 83.873
DAM_LAT = 21.525

# Approximate downstream extent per severity (degrees longitude from dam)
_EXTENT_PARAMS = {
    # (reach_lon_deg, avg_half_width_deg, max_depth_m, max_velocity_mps, area_km2)
    "Small":   (0.25,  0.015,  2.5,  1.8,  8.2),
    "Medium":  (0.50,  0.025,  5.8,  3.4,  19.7),
    "Severe":  (0.80,  0.040, 10.2,  6.1,  38.5),
}


def flood_extent_geojson(
    breach_width_m: float,
    breach_depth_m: float,
    duration_min: float,
    time_fraction: float = 1.0,
) -> dict:
    """
    Generate a GeoJSON Polygon representing the flood inundation extent.

    Parameters
    ----------
    breach_width_m, breach_depth_m, duration_min :
        Scenario parameters used to interpolate severity.
    time_fraction : float
        0.0 = start of simulation, 1.0 = end.  Used for timeline playback.
    """
    severity_key, scale = _classify_severity(breach_width_m, breach_depth_m)
    reach_lon, half_width, *_ = _EXTENT_PARAMS[severity_key]

    # Shrink extent according to time_fraction
    reach_lon = reach_lon * time_fraction
    half_width = half_width * (0.3 + 0.7 * time_fraction)

    polygon = _build_flood_polygon(reach_lon, half_width)
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [polygon]},
                "properties": {
                    "name": "Flood Inundation Extent",
                    "severity": severity_key,
                    "time_fraction": round(time_fraction, 2),
                    "data_source": "DEMO — not real ANUGA output",
                },
            }
        ],
    }


def flood_metrics(breach_width_m: float, breach_depth_m: float) -> dict:
    """Return illustrative flood metrics for a given breach configuration."""
    severity_key, scale = _classify_severity(breach_width_m, breach_depth_m)
    _, _, max_depth, max_vel, area = _EXTENT_PARAMS[severity_key]
    # Interpolate linearly within the severity band
    return {
        "max_water_depth_m": round(max_depth * scale, 2),
        "max_velocity_mps": round(max_vel * scale, 2),
        "flooded_area_km2": round(area * scale, 2),
    }


def time_series(
    breach_width_m: float,
    breach_depth_m: float,
    duration_min: float,
    n_steps: int = 12,
) -> tuple[list[float], list[float], list[float]]:
    """
    Generate illustrative time-series data for the timeline playback.

    Returns
    -------
    (time_steps, depth_at_steps, area_at_steps)
    """
    metrics = flood_metrics(breach_width_m, breach_depth_m)
    max_d = metrics["max_water_depth_m"]
    max_a = metrics["flooded_area_km2"]

    times = [round(duration_min * i / (n_steps - 1), 1) for i in range(n_steps)]
    # Logistic-like rise then slight recession
    depths = [round(max_d * _rise_curve(i / (n_steps - 1)), 2) for i in range(n_steps)]
    areas = [round(max_a * _rise_curve(i / (n_steps - 1)), 2) for i in range(n_steps)]
    return times, depths, areas


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _classify_severity(breach_width_m: float, breach_depth_m: float):
    """Map breach parameters to a severity label and a 0–1 scale factor."""
    score = breach_width_m / 60.0 * 0.6 + breach_depth_m / 25.0 * 0.4
    score = max(0.1, min(score, 1.5))
    if score < 0.45:
        return "Small", score / 0.45
    elif score < 0.85:
        return "Medium", (score - 0.45) / 0.40
    else:
        return "Severe", min(1.0, (score - 0.85) / 0.65 + 0.5)


def _build_flood_polygon(
    reach_lon: float, half_width: float
) -> list[list[float]]:
    """
    Build a tapering flood corridor polygon along the Mahanadi River.

    The polygon starts at the dam (DAM_LON, DAM_LAT) and fans out
    downstream to (DAM_LON + reach_lon, DAM_LAT - 0.20) with the given
    half-width.  A simple teardrop / wedge shape is used.
    """
    n_pts = 20
    coords = []

    # Upper bank (north side)
    for i in range(n_pts + 1):
        t = i / n_pts
        lon = DAM_LON + reach_lon * t
        lat = DAM_LAT - 0.18 * t  # river slopes slightly south
        width = half_width * math.sqrt(t + 0.05)  # widen downstream
        coords.append([round(lon, 5), round(lat + width, 5)])

    # Lower bank (south side, reversed)
    for i in range(n_pts, -1, -1):
        t = i / n_pts
        lon = DAM_LON + reach_lon * t
        lat = DAM_LAT - 0.18 * t
        width = half_width * math.sqrt(t + 0.05)
        coords.append([round(lon, 5), round(lat - width, 5)])

    # Close polygon
    coords.append(coords[0])
    return coords


def _rise_curve(t: float) -> float:
    """S-shaped rise curve from 0 → 1, slight recession near end."""
    if t < 0.7:
        return 3 * t ** 2 - 2 * t ** 3  # smoothstep
    else:
        return 1.0 - 0.08 * (t - 0.7) / 0.3  # 8 % recession
