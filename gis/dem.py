"""
Synthetic DEM (Digital Elevation Model) stub for the Hirakud Dam study area.

Generates a plausible elevation surface as a NumPy array for visualization
and domain setup.  This is NOT real terrain data.

⚠️  DEMO DATA — Replace with actual DEM (GeoTIFF, SRTM, CARTODEM, etc.)
for production use.  The real ANUGA simulation requires an accurate DEM.

Real DEM sources for this region:
- CARTODEM v3 (ISRO, 30m resolution)
- SRTM 1-Arc-Second (NASA, ~30m)
- ALOS PALSAR (JAXA, 12.5m)
"""
from __future__ import annotations
import numpy as np


# Study area bounds (EPSG:4326)
MIN_LAT, MAX_LAT = 21.30, 21.75
MIN_LON, MAX_LON = 83.70, 84.60

# Resolution
N_ROWS = 90
N_COLS = 180


def generate_synthetic_dem() -> tuple[np.ndarray, dict]:
    """
    Generate a synthetic elevation raster for the Hirakud downstream corridor.

    The terrain is modelled as:
    - High terrain (~ 200–350 m) at the western edge near the dam
    - Valley floor (~ 150–180 m) along the river channel
    - Gentle slope heading east / downstream

    Returns
    -------
    dem : np.ndarray, shape (N_ROWS, N_COLS)
        Elevation in metres (illustrative).
    meta : dict
        Raster metadata compatible with rasterio conventions.
    """
    lats = np.linspace(MAX_LAT, MIN_LAT, N_ROWS)   # top → bottom
    lons = np.linspace(MIN_LON, MAX_LON, N_COLS)
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Base elevation: slopes gently eastward (downstream)
    base = 350.0 - (lon_grid - MIN_LON) / (MAX_LON - MIN_LON) * 130.0

    # River valley: low depression along river centreline
    river_lat = 21.525 - (lon_grid - MIN_LON) / (MAX_LON - MIN_LON) * 0.18
    river_dist = np.abs(lat_grid - river_lat)
    valley = -25.0 * np.exp(-river_dist ** 2 / 0.003)

    # Add gentle random terrain variation
    rng = np.random.default_rng(seed=42)
    noise = rng.normal(0, 3, size=(N_ROWS, N_COLS))

    dem = base + valley + noise
    dem = np.clip(dem, 140.0, 380.0)

    meta = {
        "driver": "GTiff",
        "dtype": "float32",
        "crs": "EPSG:4326",
        "count": 1,
        "height": N_ROWS,
        "width": N_COLS,
        "bounds": {
            "left": MIN_LON,
            "bottom": MIN_LAT,
            "right": MAX_LON,
            "top": MAX_LAT,
        },
        "resolution_deg": (MAX_LON - MIN_LON) / N_COLS,
        "source": "Synthetic — not real terrain data",
    }
    return dem.astype(np.float32), meta


def dem_stats(dem: np.ndarray) -> dict:
    """Return basic statistics from a DEM array."""
    return {
        "min_m": float(np.min(dem)),
        "max_m": float(np.max(dem)),
        "mean_m": float(np.mean(dem)),
        "std_m": float(np.std(dem)),
        "shape": dem.shape,
    }
