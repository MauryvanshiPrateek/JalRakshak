# JalRakshak — Files Required for Vibe Coding

This document tells an AI coding agent what files should exist before implementation.

## A. Core specification files — REQUIRED

- `README.md` — project overview and setup
- `TECH_STACK.md` — technologies and architecture rules
- `ARCHITECTURE.md` — system/data flow
- `UI_INFO.md` — screen-by-screen UI specification
- `requirements.txt` — Python dependencies
- `Dockerfile` — reproducible environment
- `FILES_FOR_VIBE_CODING.md` — this implementation guide

## B. Files strongly recommended

### `docs/PRODUCT_REQUIREMENTS.md`
Explain:
- problem
- target users
- user journeys
- MVP
- non-MVP
- success criteria

### `docs/SCIENTIFIC_MODEL.md`
Document:
- dam-break assumptions
- breach parameters
- shallow-water modelling assumptions
- initial/boundary conditions
- units
- expected ANUGA inputs/outputs
- limitations

This is especially important because the project is a hydrodynamic modelling system.

### `docs/DATA_SPECIFICATION.md`
Define:
- DEM requirements
- CRS
- raster resolution
- river geometry
- dam geometry
- settlement data
- roads
- population/exposure data
- accepted file formats

### `docs/API_AND_DATA_CONTRACTS.md`
Define the exact Python dictionaries/JSON objects exchanged between:
- UI
- simulation service
- GIS service
- risk service

### `docs/DEMO_SCENARIO.md`
Create one reproducible SIH demonstration scenario:
- study area
- input dataset names
- dam
- breach parameters
- expected outputs
- expected screenshots/KPIs

### `config/scenarios.yaml`
Store scenario presets instead of hard-coding them in UI code.

### `.env.example`
For optional:
- data API keys
- external services
- storage
- database configuration

Never commit real secrets.

## C. Data folders

```text
data/
├── raw/
├── processed/
├── sample/
└── README.md
```

`data/README.md` should explain where each dataset belongs and its CRS/license/source.

## D. Application files

```text
app/
├── main.py
├── components/
│   ├── sidebar.py
│   ├── map_view.py
│   ├── kpis.py
│   ├── charts.py
│   └── warnings.py
└── pages/
    ├── dashboard.py
    ├── scenario.py
    └── results.py
```

## E. Simulation files

```text
simulation/
├── __init__.py
├── models.py
├── breach_model.py
├── anuga_runner.py
├── mock_runner.py
└── simulation_service.py
```

`mock_runner.py` is useful only during UI development.

## F. GIS files

```text
gis/
├── __init__.py
├── dem.py
├── domain.py
├── raster.py
├── vector.py
├── flood_extent.py
└── risk.py
```

## G. Data models

Recommended:

```text
models/
├── scenario.py
├── simulation_result.py
└── layers.py
```

Use typed Python models/dataclasses or Pydantic.

## H. Tests

```text
tests/
├── test_breach_model.py
├── test_gis.py
├── test_risk.py
├── test_scenario_validation.py
└── test_simulation_contract.py
```

## I. Developer files

Recommended:
- `.gitignore`
- `.dockerignore`
- `pyproject.toml` or `pytest.ini`
- `docker-compose.yml` only if multiple services are introduced
- `Makefile` or simple scripts for common commands

## J. What the AI coding agent must NOT invent

The coding agent must not invent:
- real-world flood results
- population numbers
- dam dimensions
- DEM characteristics
- scientific validation metrics
- API credentials
- claims that the system is operationally real-time

If real data is missing, use clearly labelled sample/mock data.

## K. Vibe-Coding Prompt Order

Give the AI coding agent these files in this order:

1. `README.md`
2. `TECH_STACK.md`
3. `ARCHITECTURE.md`
4. `UI_INFO.md`
5. `docs/PRODUCT_REQUIREMENTS.md`
6. `docs/SCIENTIFIC_MODEL.md`
7. `docs/DATA_SPECIFICATION.md`
8. `docs/API_AND_DATA_CONTRACTS.md`
9. `docs/DEMO_SCENARIO.md`
10. `config/scenarios.yaml`
11. `requirements.txt`
12. `Dockerfile`

Then ask it to implement the project in phases.

## L. Recommended Coding Phases

### Phase 1
Create Streamlit UI using mock simulation output.

### Phase 2
Implement GIS layer loading and map controls.

### Phase 3
Implement scenario validation and configuration.

### Phase 4
Integrate real ANUGA.

### Phase 5
Post-process ANUGA output into flood layers.

### Phase 6
Implement exposure/risk analysis.

### Phase 7
Implement timeline/playback.

### Phase 8
Add tests, Docker, error handling and documentation.

### Phase 9
Run a complete end-to-end demo using one reproducible study area.
