"""
Breach parameter calculations for dam-break scenarios.

⚠️  IMPORTANT SCIENTIFIC NOTE:
All formulae here are simplified illustrative approximations used for the
prototype UI only.  They are NOT validated hydraulic models.  The real
simulation is performed by ANUGA (Phase 4+).

Peak discharge estimate uses the simplified broad-crested weir equation:
    Q_peak ≈ Cd × B × (2/3) × sqrt(2g/3) × H^(3/2)
where:
    Cd  ≈ 0.5  (illustrative discharge coefficient — not calibrated)
    B   = breach width (m)
    H   = reservoir head above breach invert (m)
    g   = 9.81 m/s²
"""
from __future__ import annotations
import math


# ---------------------------------------------------------------------------
# Constants (illustrative only — see module docstring)
# ---------------------------------------------------------------------------
GRAVITY_MS2 = 9.81
DISCHARGE_COEFFICIENT = 0.5   # Cd — illustrative, not calibrated


def peak_discharge_m3s(
    breach_width_m: float,
    reservoir_head_m: float,
) -> float:
    """
    Estimate peak breach discharge using the simplified weir formula.

    Parameters
    ----------
    breach_width_m : float
        Width of the breach opening (m).
    reservoir_head_m : float
        Water head above the breach invert (m), i.e. reservoir level
        minus bottom of breach.

    Returns
    -------
    float
        Illustrative peak discharge in m³/s.

    Notes
    -----
    This is a rough upper-bound estimate used for UI display only.
    Do not use for engineering decision-making.
    """
    if breach_width_m <= 0 or reservoir_head_m <= 0:
        return 0.0
    weir_coeff = DISCHARGE_COEFFICIENT * (2.0 / 3.0) * math.sqrt(2.0 * GRAVITY_MS2 / 3.0)
    return weir_coeff * breach_width_m * (reservoir_head_m ** 1.5)


def breach_volume_m3(
    breach_width_m: float,
    breach_depth_m: float,
    reservoir_surface_area_km2: float = 743.0,  # Hirakud approximate
) -> float:
    """
    Very rough estimate of water volume released through breach (m³).

    Assumes a trapezoidal breach cross-section and that water level drops
    by breach_depth_m over the full reservoir surface area.

    Parameters
    ----------
    reservoir_surface_area_km2 : float
        Reservoir surface area in km².  Defaults to Hirakud approximate.
    """
    area_m2 = reservoir_surface_area_km2 * 1e6
    # Approximate: triangle in depth profile
    return 0.5 * area_m2 * breach_depth_m


def time_to_peak_s(formation_time_min: float) -> float:
    """
    Estimate time-to-peak discharge.

    Simplified assumption: peak occurs at the end of breach formation.
    """
    return formation_time_min * 60.0


def flooded_area_km2_estimate(
    breach_width_m: float,
    breach_depth_m: float,
    duration_min: float,
    downstream_slope: float = 0.002,  # approximate Mahanadi gradient
) -> float:
    """
    Very rough downstream flood area estimate.

    Uses: Area ≈ Q_peak × duration / average_depth
    This is for UI illustration only.
    """
    head = breach_depth_m
    q = peak_discharge_m3s(breach_width_m, head)
    duration_s = duration_min * 60.0
    volume_m3 = q * duration_s * 0.3   # factor < 1: not all flow reaches flat area
    avg_depth_m = max(0.5, breach_depth_m * 0.15)
    area_m2 = volume_m3 / avg_depth_m
    return round(area_m2 / 1e6, 2)


def warning_level(max_depth_m: float) -> str:
    """Classify flood warning level from maximum water depth."""
    if max_depth_m < 0.5:
        return "Low"
    elif max_depth_m < 2.0:
        return "Moderate"
    elif max_depth_m < 5.0:
        return "High"
    else:
        return "Critical"
