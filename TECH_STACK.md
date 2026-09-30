# JalRakshak — Technology Stack

## Frontend / UI
- Python
- Streamlit
- Folium / Leaflet for interactive maps
- Plotly for charts
- HTML/CSS only where needed for UI polish

## Hydrodynamic Modelling
- ANUGA Hydro
- NumPy
- SciPy where required

## GIS / Geospatial Processing
- GeoPandas
- Rasterio
- Shapely
- PyProj
- Fiona
- Folium

## Data
- DEM/elevation raster
- River and dam vector data
- Settlement/building/road layers
- Optional satellite imagery
- GeoJSON / GeoTIFF / Shapefile / CSV

## Backend Architecture
The prototype can remain a Streamlit application initially.

Recommended service modules:
- Simulation Service
- GIS Processing Service
- Risk Analysis Service
- Data Service
- Export Service

FastAPI is optional if the team later separates the frontend and backend.

## Storage
MVP:
- Local files
- SQLite for simulation metadata

Scale-up:
- PostgreSQL
- PostGIS for spatial data

## DevOps
- Git
- GitHub
- Docker
- Docker Compose for multi-service development
- Linux recommended for the ANUGA development environment

## Testing
- pytest
- lightweight unit tests for GIS/risk calculations
- scenario regression tests for simulation outputs

## Visualization
- Interactive map
- Flood-depth layer
- Flood-extent polygon
- Risk zones
- Time slider
- KPI cards
- Charts

## Architecture Rule

Do not put ANUGA execution, GIS processing and UI code in one file. Keep them behind service interfaces so the UI can first use sample/mock outputs and later switch to real simulation outputs.
