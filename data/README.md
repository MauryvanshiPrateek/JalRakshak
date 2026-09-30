# JalRakshak — Data Directory

## Folder Structure

```
data/
├── raw/         # Original unprocessed datasets (DEM, shapefiles, etc.)
├── processed/   # Clipped, reprojected, or derived datasets
├── sample/      # Sample/mock data for demo and development
└── README.md    # This file
```

## CRS Policy

All spatial datasets must be documented with their Coordinate Reference System (CRS).
Before distance or area calculations, transform all layers to a common projected CRS
appropriate for the study area (e.g., UTM Zone 44N — EPSG:32644 for Odisha, India).

## Data Licensing

Record the source, date, and license for every externally obtained dataset.
Never commit datasets with restrictive licenses without permission.

## What goes where

| Folder | Contents |
|--------|----------|
| `raw/` | Original files as downloaded (SRTM DEM, OSM shapefiles, etc.) |
| `processed/` | Clipped, resampled, reprojected, or merged files |
| `sample/` | Synthetic or public-domain files used for demo/testing |

## Phase 1 Demo Data

The Phase 1 prototype uses **synthetic/illustrative data** generated in Python
(see `gis/` modules). No real datasets are required to run the demo.

When real data is available, place it in `raw/` and update `gis/dem.py` and
`gis/vector.py` to load it instead of the generated placeholders.

## Suggested Real Data Sources (India)

| Dataset | Source | Format | Notes |
|---------|--------|--------|-------|
| DEM | CARTODEM v3 (NRSC/ISRO) | GeoTIFF | 30 m resolution |
| DEM (alt) | SRTM 1-Arc-Second (NASA) | GeoTIFF | ~30 m, global |
| River network | WRIS India | Shapefile | River centre lines |
| Administrative boundaries | Survey of India | Shapefile | District/state |
| Roads | OpenStreetMap | GeoJSON | Community-maintained |
| Settlements | Census of India / OSM | CSV / GeoJSON | Population data |
