"""
Raster utility stubs for JalRakshak GIS processing.

In Phase 4+ these will use rasterio to read/write real GeoTIFFs.
For Phase 1–3 they provide no-op stubs so the UI can run without
rasterio being installed in non-Linux environments.
"""
from __future__ import annotations


def save_array_as_geotiff(array, filepath: str, meta: dict) -> bool:
    """
    Write a NumPy array as a GeoTIFF.

    Returns True on success, False if rasterio is not available.
    """
    try:
        import rasterio
        from rasterio.transform import from_bounds
        import numpy as np

        bounds = meta.get("bounds", {})
        transform = from_bounds(
            bounds.get("left", 0), bounds.get("bottom", 0),
            bounds.get("right", 1), bounds.get("top", 1),
            meta.get("width", array.shape[1]),
            meta.get("height", array.shape[0]),
        )
        with rasterio.open(
            filepath, "w",
            driver="GTiff",
            height=array.shape[0],
            width=array.shape[1],
            count=1,
            dtype=str(array.dtype),
            crs=meta.get("crs", "EPSG:4326"),
            transform=transform,
        ) as dst:
            dst.write(array, 1)
        return True
    except ImportError:
        return False


def load_geotiff(filepath: str):
    """
    Load a GeoTIFF as a NumPy array.

    Returns (array, meta) or (None, None) if rasterio unavailable.
    """
    try:
        import rasterio
        with rasterio.open(filepath) as src:
            data = src.read(1)
            meta = src.meta.copy()
        return data, meta
    except ImportError:
        return None, None
