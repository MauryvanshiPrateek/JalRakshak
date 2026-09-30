# JalRakshak — System Architecture

## 1. High-Level Architecture

```text
┌───────────────────────────────────────────────┐
│                 STREAMLIT UI                  │
│ Scenario | Map | KPIs | Charts | Warnings     │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│              APPLICATION SERVICES             │
│ Simulation | GIS | Risk | Data | Export       │
└───────┬──────────────────┬────────────────────┘
        │                  │
        ▼                  ▼
┌───────────────┐    ┌─────────────────────────┐
│ ANUGA Adapter │    │ GIS Processing           │
│               │    │ DEM/Raster/Vector        │
└───────┬───────┘    └────────────┬────────────┘
        │                         │
        ▼                         ▼
┌────────────────┐       ┌──────────────────────┐
│ Hydro Outputs  │       │ Risk / Exposure      │
│ depth velocity │       │ settlements roads    │
│ stage extent   │       │ population etc.      │
└────────┬───────┘       └──────────┬───────────┘
         └──────────────┬───────────┘
                        ▼
              ┌──────────────────┐
              │ Result Layers    │
              │ GeoTIFF/GeoJSON  │
              └────────┬─────────┘
                       ▼
              Interactive Map
```

## 2. Data Flow

### Inputs
- Dam location
- River geometry
- DEM
- Reservoir/water condition
- Breach parameters
- Simulation duration
- Optional exposure layers

### Processing
1. Validate inputs.
2. Clip DEM to study area.
3. Prepare terrain/domain.
4. Generate computational mesh/domain.
5. Configure initial/boundary conditions.
6. Run ANUGA.
7. Extract water depth, velocity and related outputs.
8. Convert outputs to GIS layers.
9. Intersect flood layers with exposure data.
10. Calculate risk/exposure indicators.
11. Render results.

## 3. Recommended Python Interfaces

```python
class SimulationEngine:
    def run(self, scenario):
        ...

class GISProcessor:
    def prepare_domain(self, dem, bounds):
        ...

class RiskEngine:
    def calculate(self, flood_layer, exposure_layers):
        ...
```

Implement:

```text
SimulationEngine
 ├── MockSimulationEngine   # UI development
 └── AnugaSimulationEngine  # real prototype

GISProcessor
RiskEngine
```

## 4. Simulation Lifecycle

```text
CREATED
   ↓
VALIDATED
   ↓
PREPARING
   ↓
RUNNING
   ↓
POST_PROCESSING
   ↓
COMPLETED
```

Failure state:

```text
ANY STATE → FAILED
```

The UI should display useful error messages instead of Python tracebacks.

## 5. Output Contract

A completed simulation should expose:

```text
simulation_id
scenario_name
duration
max_water_depth
max_velocity
flooded_area
flood_extent_layer
depth_layer
velocity_layer
risk_layer
affected_settlements
affected_roads
```

## 6. Scalability

The MVP can execute simulations locally.

Later:

```text
Streamlit
    ↓
FastAPI
    ↓
Job Queue
    ↓
Simulation Worker
    ↓
ANUGA
    ↓
Object Storage / PostGIS
```

This prevents long-running simulations from blocking the web UI.

## 7. Important Design Decision

Separate:
- simulation physics,
- geospatial processing,
- risk calculation,
- presentation.

This allows each part to be tested independently.
